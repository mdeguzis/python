#!/usr/bin/env python3
"""
media-sorter.py - Automatically sort downloaded media files into organized folders.

Scans a downloads directory and moves content to movies/, tv-shows/, music/,
or photos/ based on filename patterns and file extensions.

Designed to run every 15 minutes via crontab:
    */15 * * * * /usr/bin/python3 /home/mikeyd/src/python/utilities/media-sorter.py
"""

import argparse
import logging
import os
import re
import shutil
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

DEFAULT_SOURCE_DIR = "/mnt/nvidia-shield/media/downloads"
DEFAULT_DEST_DIR = "/mnt/nvidia-shield/media"

# Standard subdirectories expected under the destination root
MEDIA_SUBDIRS = ["movies", "tv-shows", "music", "photos", "home-videos"]
DEFAULT_LOG_DIR = os.path.expanduser("~/logs/media-sorter")
LOG_RETENTION_DAYS = 30

# ---------------------------------------------------------------------------
# File-type extension sets
# ---------------------------------------------------------------------------

MUSIC_EXTENSIONS = {".mp3", ".flac", ".m4a", ".aac", ".ogg", ".wav", ".wma", ".opus", ".ape", ".alac"}
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".raw", ".cr2", ".nef", ".heic", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".m4v", ".ts", ".m2ts", ".iso", ".vob", ".mpg", ".mpeg"}

# ---------------------------------------------------------------------------
# Detection patterns
# ---------------------------------------------------------------------------

# TV show markers (checked before movie heuristics — more specific)
TV_PATTERNS = [
    re.compile(r'[Ss]\d{1,2}[Ee]\d{1,2}'),          # S01E01, s2e3
    re.compile(r'\b\d{1,2}[xX]\d{2}\b'),              # 1x01
    re.compile(r'\bSeason\s+\d+\b', re.IGNORECASE),   # Season 1
    re.compile(r'\bComplete[\s._-]+Series\b', re.IGNORECASE),
    re.compile(r'\bMini[\s._-]?Series\b', re.IGNORECASE),
    re.compile(r'\bEpisode\s+\d+\b', re.IGNORECASE),
]

# Year in (YYYY), [YYYY], or .YYYY. — used to confirm a movie
MOVIE_YEAR_PATTERN = re.compile(r'[\(\[._](\d{4})[\)\]._]')

# Source/quality tags that indicate a video release
VIDEO_RELEASE_MARKERS = re.compile(
    r'\b(bluray|blu[\s._-]?ray|webrip|web[\s._-]?dl|dvdrip|hdtv|bdrip|'
    r'1080p|720p|2160p|4k|uhd|x264|x265|hevc|xvid|divx|yts|rarbg|'
    r'hdrip|remux|proper|repack|extended|theatrical)\b',
    re.IGNORECASE,
)

VALID_YEAR_RANGE = range(1888, 2100)  # first film ever made to far future


def _year_is_valid(match: re.Match) -> bool:
    return int(match.group(1)) in VALID_YEAR_RANGE


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logger = logging.getLogger("media_sorter")


class _TqdmLoggingHandler(logging.StreamHandler):
    """Routes log output through tqdm.write() so bars and log lines don't collide."""

    def emit(self, record: logging.LogRecord) -> None:
        from tqdm import tqdm
        try:
            tqdm.write(self.format(record))
        except Exception:
            self.handleError(record)


def initialize_logger(
    log_level: int = logging.INFO,
    log_filename: str | None = None,
    propagate: bool = False,
    scope: str | None = None,
    formatter: str = "%(asctime)s - %(levelname)s - %(message)s",
) -> logging.Logger:
    """Initialize logger for stdout and optional rotating file output.

    Levels:
      default      → INFO   (moves, skips, errors)
      -v/--verbose → DEBUG  (detected type + TMDb results per entry)
      -D/--debug   → DEBUG  (same, plus every file scanned and pattern tested)
    """
    if log_level == logging.DEBUG:
        formatter = "[%(name)s] %(asctime)s - %(levelname)s - %(message)s"

    _logger = logging.getLogger(scope)
    _logger.setLevel(log_level)
    _logger.propagate = propagate

    fmt = logging.Formatter(formatter, datefmt="%Y-%m-%dT%H:%M:%SZ")
    fmt.converter = time.gmtime  # UTC

    console_handler = _TqdmLoggingHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(fmt)
    _logger.addHandler(console_handler)

    if log_filename:
        log_path = Path(log_filename).parent
        log_path.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_filename, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(fmt)
        _logger.addHandler(file_handler)

    return _logger


# ---------------------------------------------------------------------------
# Exclusion helpers
# ---------------------------------------------------------------------------


def load_exclusions(args_excludes: list[str] | None, exclude_from: str | None) -> list[re.Pattern]:
    """
    Build a list of compiled regex patterns from:
      - individual --exclude PATTERN arguments
      - a --exclude-from FILE (one pattern per line; # = comment)
    """
    raw: list[str] = list(args_excludes or [])

    if exclude_from:
        p = Path(exclude_from)
        if not p.is_file():
            print(f"Warning: --exclude-from file not found: {p}", file=sys.stderr)
        else:
            with open(p) as f:
                for lineno, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith("#"):
                        raw.append(line)

    patterns: list[re.Pattern] = []
    for expr in raw:
        try:
            patterns.append(re.compile(expr))
        except re.error as exc:
            print(f"Warning: invalid exclusion pattern '{expr}': {exc}", file=sys.stderr)

    return patterns


def is_excluded(name: str, patterns: list[re.Pattern]) -> bool:
    return any(p.search(name) for p in patterns)


# ---------------------------------------------------------------------------
# Media type detection
# ---------------------------------------------------------------------------


def _classify_directory_content(path: Path, debug: bool, logger: logging.Logger) -> str | None:
    """
    Classify the primary content type of a directory by inspecting its files.

    Precedence (highest to lowest):
      video  >  music  >  photos

    A single video file beats any number of thumbnail/poster images, which
    is the common case for YTS-style movie folders that include a .jpg cover.
    """
    has_video = has_music = has_photo = False
    for f in path.rglob("*"):
        if not f.is_file():
            continue
        ext = f.suffix.lower()
        if debug:
            logger.debug("  scanning file: %s  (ext=%s)", f.name, ext or "<none>")
        if ext in VIDEO_EXTENSIONS:
            has_video = True
            if debug:
                logger.debug("  video file found — stopping directory scan")
            break          # video wins immediately — no need to keep scanning
        if ext in MUSIC_EXTENSIONS:
            has_music = True
        elif ext in PHOTO_EXTENSIONS:
            has_photo = True

    if has_video:
        return "video"
    if has_music:
        return "music"
    if has_photo:
        return "photos"
    return None


def detect_media_type(name: str, path: Path, debug: bool, logger: logging.Logger) -> str | None:
    """
    Classify *path* (file or directory) as one of:
        'movies', 'tv-shows', 'music', 'photos'
    Returns None when the type cannot be determined.

    Priority order:
        1. TV show patterns  (most specific)
        2. Extension / dominant-extension checks
        3. Movie year + release-marker heuristics
    """
    if debug:
        logger.debug("detecting type for: %s", name)

    # 1. TV show patterns take precedence over everything
    for pattern in TV_PATTERNS:
        m = pattern.search(name)
        if debug:
            logger.debug("  tv pattern %-30s → %s", pattern.pattern, f"MATCH '{m.group()}'" if m else "no match")
        if m:
            return "tv-shows"

    # 2. Single file — decide by extension
    if path.is_file():
        ext = path.suffix.lower()
        if debug:
            logger.debug("  single file, ext=%s", ext or "<none>")
        if ext in MUSIC_EXTENSIONS:
            return "music"
        if ext in PHOTO_EXTENSIONS:
            return "photos"
        if ext in VIDEO_EXTENSIONS:
            return "movies"
        return None

    # 3. Directory — inspect content types (video beats photos/thumbnails)
    if debug:
        logger.debug("  directory — scanning contents of: %s", path)
    content_type = _classify_directory_content(path, debug, logger)
    if debug:
        logger.debug("  directory content type: %s", content_type or "unknown")

    if content_type == "music":
        return "music"
    if content_type == "photos":
        return "photos"

    if content_type == "video" or content_type is None:
        # Check for movie year in folder name
        year_match = MOVIE_YEAR_PATTERN.search(name)
        if debug:
            logger.debug("  year pattern match: %s", year_match.group(1) if year_match else "none")
        if year_match and _year_is_valid(year_match):
            return "movies"
        # Release/quality markers (WEBRip, YTS, 1080p, etc.)
        rm = VIDEO_RELEASE_MARKERS.search(name)
        if debug:
            logger.debug("  release marker match: %s", rm.group() if rm else "none")
        if rm:
            return "movies"
        # Video directory with no other clues — fall back to movies
        if content_type == "video":
            return "movies"

    return None


# ---------------------------------------------------------------------------
# TMDb lookup
# ---------------------------------------------------------------------------

# Junk to strip before sending a title to TMDb
_TITLE_JUNK = re.compile(
    r'[\(\[]((?:19|20)\d{2})[\)\]].*$'          # (1998) and everything after
    r'|[._]((?:19|20)\d{2})[._].*$'             # .1998. and everything after
    r'|\b(19|20)\d{2}\b.*$',                     # bare year and everything after
    re.IGNORECASE,
)
_SEP_CLEANUP = re.compile(r'[._]')


def _extract_title_year(name: str) -> tuple[str, str | None]:
    """Return (clean_title, year_str) parsed from a folder/file name."""
    year: str | None = None

    # Year in brackets: (1998) or [1998]
    m = re.search(r'[\(\[]((?:19|20)\d{2})[\)\]]', name)
    if m:
        year = m.group(1)
        title_raw = name[:m.start()]
    else:
        # Year between separators: .1998. or _1998_
        m = re.search(r'[._]((?:19|20)\d{2})[._]', name)
        if m:
            year = m.group(1)
            title_raw = name[:m.start()]
        else:
            title_raw = name

    title = _SEP_CLEANUP.sub(" ", title_raw).strip(" -_[](){}").strip()
    return title, year


def tmdb_lookup(name: str, api_key: str, logger: logging.Logger) -> str | None:
    """
    Query the TMDb search/multi endpoint and return 'movies' or 'tv-shows'.
    Returns None on no result or any network/API error.
    """
    import json
    import urllib.error
    import urllib.parse
    import urllib.request

    title, year = _extract_title_year(name)
    if not title:
        logger.debug("TMDb: could not extract title from %r — skipping", name)
        return None

    params: dict[str, str] = {"api_key": api_key, "query": title}
    if year:
        params["year"] = year

    url = "https://api.themoviedb.org/3/search/multi?" + urllib.parse.urlencode(params)
    safe_url = url.replace(api_key, "***")  # never log the real key

    logger.debug("TMDb request: GET %s", safe_url)
    logger.debug("TMDb query params: title=%r year=%s", title, year or "—")

    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            status = resp.status
            headers = dict(resp.headers)
            raw = resp.read()
    except urllib.error.HTTPError as exc:
        logger.debug("TMDb HTTP error: %s %s", exc.code, exc.reason)
        return None
    except Exception as exc:
        logger.debug("TMDb request failed: %s: %s", type(exc).__name__, exc)
        return None

    logger.debug("TMDb response: HTTP %s  content-type=%s  bytes=%d",
                 status, headers.get("Content-Type", "?"), len(raw))

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.debug("TMDb response JSON parse error: %s", exc)
        return None

    total = data.get("total_results", 0)
    logger.debug("TMDb response body: total_results=%d  results_in_page=%d",
                 total, len(data.get("results", [])))

    results = [r for r in data.get("results", []) if r.get("media_type") in ("movie", "tv")]
    if not results:
        logger.debug("TMDb: no movie/tv results for %r (total hits: %d)", title, total)
        return None

    for i, r in enumerate(results[:3]):  # log up to 3 candidates
        logger.debug(
            "TMDb candidate[%d]: type=%-5s  id=%-8s  title=%r  year=%s  popularity=%.1f",
            i,
            r.get("media_type", "?"),
            r.get("id", "?"),
            r.get("title") or r.get("name", "?"),
            (r.get("release_date") or r.get("first_air_date") or "?")[:4],
            r.get("popularity", 0.0),
        )

    top = results[0]
    media_type = top["media_type"]
    tmdb_title = top.get("title") or top.get("name", "?")
    tmdb_year = (top.get("release_date") or top.get("first_air_date") or "")[:4]
    logger.debug("TMDb selected: %s → %r (%s)", media_type, tmdb_title, tmdb_year or "?")

    return "movies" if media_type == "movie" else "tv-shows"


# ---------------------------------------------------------------------------
# File-system operations
# ---------------------------------------------------------------------------


def _merge_into(src: Path, dest: Path, overwrite: bool, logger: logging.Logger) -> bool:
    """Sync missing files from *src* directory into an existing *dest* directory.

    Files already present in *dest* are skipped (or overwritten if *overwrite*).
    The source directory is removed once empty.  Returns True if no errors occurred.
    """
    added = skipped = errors = 0

    for item in src.iterdir():
        dest_item = dest / item.name
        if dest_item.exists():
            if not overwrite:
                logger.info("  Already exists, skipping: %s", item.name)
                skipped += 1
                continue
            logger.info("  Overwriting: %s", item.name)
            if dest_item.is_dir():
                shutil.rmtree(dest_item)
            else:
                dest_item.unlink()
        try:
            shutil.move(str(item), str(dest_item))
            logger.info("  Added to existing folder: %s -> %s/", item.name, dest.name)
            added += 1
        except OSError as exc:
            logger.error("  Failed to move '%s': %s", item, exc)
            errors += 1

    # Remove source dir if now empty
    try:
        if not any(src.iterdir()):
            src.rmdir()
            logger.debug("Removed empty source folder: %s", src.name)
    except OSError:
        pass

    logger.info(
        "Merged: %s  ->  %s/  (added: %d  skipped: %d%s)",
        src.name, dest, added, skipped,
        f"  errors: {errors}" if errors else "",
    )
    return errors == 0


def move_item(
    src: Path,
    media_dir: Path,
    media_type: str,
    overwrite: bool,
    logger: logging.Logger,
) -> bool:
    """Move *src* into *media_dir*/<media_type>/. Returns True on success.

    When *dest* is an existing directory and *src* is also a directory, the
    contents are merged (rsync-style): only files missing from *dest* are moved.
    """
    dest_dir = media_dir / media_type
    dest = dest_dir / src.name

    # Directory already exists at destination — merge instead of replace
    if dest.is_dir() and src.is_dir():
        logger.info("Merging into existing folder: %s", dest)
        return _merge_into(src, dest, overwrite, logger)

    if dest.exists():
        if not overwrite:
            logger.warning("Destination already exists, skipping: %s", dest)
            return False
        logger.info("Overwriting existing: %s", dest)
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()

    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))
        logger.info("Moved: %s  ->  %s/", src.name, dest_dir)
        return True
    except OSError as exc:
        logger.error("Failed to move '%s': %s", src, exc)
        return False


# ---------------------------------------------------------------------------
# Main scan loop
# ---------------------------------------------------------------------------

# A planned move: source path and its resolved destination type
MovePlan = list[tuple[Path, str]]


def build_plan(
    downloads_dir: Path,
    exclusion_patterns: list[re.Pattern],
    debug: bool,
    tmdb_key: str | None,
    logger: logging.Logger,
) -> tuple[MovePlan, int]:
    """
    Scan *downloads_dir* and classify each entry.
    Returns (plan, skipped) where plan is a list of (src, media_type) tuples.
    """
    if not downloads_dir.is_dir():
        logger.error("Downloads directory not found: %s", downloads_dir)
        return [], 0

    plan: MovePlan = []
    skipped = 0

    for item in sorted(downloads_dir.iterdir()):
        name = item.name

        if name.startswith("."):
            logger.debug("Skipping hidden entry: %s", name)
            skipped += 1
            continue

        if is_excluded(name, exclusion_patterns):
            logger.info("Excluded: %s", name)
            skipped += 1
            continue

        # TMDb is primary when key available; regex is fallback
        media_type = None
        if tmdb_key:
            media_type = tmdb_lookup(name, tmdb_key, logger)

        if media_type is None:
            regex_type = detect_media_type(name, item, debug, logger)
            if regex_type and tmdb_key:
                logger.debug("TMDb found nothing — regex fallback: %s", regex_type)
            media_type = regex_type

        if media_type is None:
            logger.warning("Unknown media type, skipping: %s", name)
            skipped += 1
            continue

        logger.debug("'%s' → %s", name, media_type)
        plan.append((item, media_type))

    return plan, skipped


def execute_plan(
    plan: MovePlan,
    dest_dir: Path,
    overwrite: bool,
    logger: logging.Logger,
) -> tuple[int, int]:
    """
    Execute a move plan with a tqdm progress bar.
    Returns (moved, errors).
    """
    from tqdm import tqdm

    moved = errors = 0

    bar = tqdm(plan, desc="Moving", unit="item", dynamic_ncols=True)
    for src, media_type in bar:
        bar.set_postfix_str(src.name[:45])
        if move_item(src, dest_dir, media_type, overwrite, logger):
            moved += 1
        else:
            errors += 1

    return moved, errors


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="media-sorter.py",
        description=(
            "Sort downloaded media files into movies/, tv-shows/, music/, or photos/ "
            "based on filename patterns and file extensions."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Normal run with defaults
  %(prog)s

  # Actually move files (dry-run is the default); confirm prompt shown unless -y
  %(prog)s --no-dry-run
  %(prog)s --no-dry-run --no-confirm

  # Show detected type per entry
  %(prog)s -v

  # Show every file scanned and every pattern tested
  %(prog)s --debug

  # Exclude sample clips and extras
  %(prog)s --exclude '\\.sample\\.' --exclude '[Ee]xtras?'

  # Load exclusions from a file (rsync-style, one pattern per line)
  %(prog)s --exclude-from ~/media_excludes.txt

  # Override source/dest directories
  %(prog)s --source /mnt/nas/incoming --destination /mnt/nas/library

  # Use TMDb for online title lookup (also reads TMDB_API_KEY env var)
  %(prog)s --tmdb-key YOUR_KEY

  # Install crontab entry (every 15 minutes)
  %(prog)s --install-cron
        """,
    )

    parser.add_argument(
        "--source", "-s",
        default=DEFAULT_SOURCE_DIR,
        metavar="DIR",
        help=f"Directory to scan for new downloads (default: {DEFAULT_SOURCE_DIR})",
    )
    parser.add_argument(
        "--destination", "-d",
        default=DEFAULT_DEST_DIR,
        metavar="DIR",
        help=f"Root media directory containing movies/, tv-shows/, etc. (default: {DEFAULT_DEST_DIR})",
    )
    parser.add_argument(
        "--log-dir", "-l",
        default=DEFAULT_LOG_DIR,
        metavar="DIR",
        help=f"Directory for rotating log files (default: {DEFAULT_LOG_DIR})",
    )
    parser.set_defaults(dry_run=True)
    parser.add_argument(
        "--no-dry-run", "-n",
        dest="dry_run",
        action="store_false",
        help="Actually move files (dry-run is on by default)",
    )
    parser.add_argument(
        "--exclude", "-e",
        action="append",
        metavar="PATTERN",
        dest="excludes",
        help=(
            "Exclude entries whose name matches this regex (can be repeated). "
            "Example: --exclude '\\.sample\\.' --exclude '[Ee]xtras?'"
        ),
    )
    parser.add_argument(
        "--exclude-from", "-E",
        metavar="FILE",
        help="Read exclusion patterns from FILE, one regex per line (# = comment)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detected type for each entry",
    )
    parser.add_argument(
        "--debug", "-D",
        action="store_true",
        help="Show every file scanned and every pattern tested (implies -v)",
    )
    parser.add_argument(
        "--tmdb-key", "-T",
        metavar="KEY",
        default=None,
        help=(
            "TMDb API key for online title lookup. "
            "Also checks TMDB_API_KEY env var and ~/.tmdb.key file. "
            "Get a free key at themoviedb.org/settings/api"
        ),
    )
    parser.add_argument(
        "--no-confirm", "-y",
        action="store_true",
        help="Skip the confirmation prompt before moving files",
    )
    parser.add_argument(
        "--overwrite", "-o",
        action="store_true",
        help="Overwrite existing destination files/folders instead of skipping",
    )
    parser.add_argument(
        "--install-cron", "-C",
        action="store_true",
        help="Install a crontab entry to run this script every 15 minutes, then exit",
    )

    return parser


def cleanup_old_logs(log_dir: str, days: int = LOG_RETENTION_DAYS) -> None:
    """Delete log files older than *days* from *log_dir*."""
    cutoff = datetime.now() - timedelta(days=days)
    for f in Path(log_dir).glob("media-sorter-*.log"):
        if datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
            f.unlink()
            logger.debug("Deleted old log: %s", f.name)


def resolve_tmdb_key(arg_key: str | None) -> str | None:
    """
    Return a TMDb API key from the first available source:
      1. --tmdb-key CLI argument
      2. TMDB_API_KEY environment variable
      3. ~/.tmdb.key file (single line)
    """
    if arg_key:
        return arg_key.strip()
    env = os.environ.get("TMDB_API_KEY", "").strip()
    if env:
        return env
    key_file = Path.home() / ".tmdb.key"
    if key_file.is_file():
        key = key_file.read_text().strip()
        if key:
            return key
    return None


def install_cron(script_path: str, args: "argparse.Namespace") -> int:
    """Add a */15 crontab entry for this script if one doesn't already exist.

    Requires --source and --destination; includes --no-dry-run, --no-confirm,
    and --overwrite if they were passed.
    """
    import subprocess

    if args.source == DEFAULT_SOURCE_DIR and "--source" not in sys.argv and "-s" not in sys.argv:
        print("Error: --source is required when using --install-cron", file=sys.stderr)
        return 1
    if args.destination == DEFAULT_DEST_DIR and "--destination" not in sys.argv and "-d" not in sys.argv:
        print("Error: --destination is required when using --install-cron", file=sys.stderr)
        return 1

    python = sys.executable
    flags = [
        f"--source {args.source}",
        f"--destination {args.destination}",
        "--no-dry-run",
        "--no-confirm",
    ]
    if args.overwrite:
        flags.append("--overwrite")

    installed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"# media-sorter — installed {installed_at} — github.com/mdeguzis/python"
    entry = f"{header}\n*/15 * * * * {python} {script_path} {' '.join(flags)}"

    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    existing = result.stdout if result.returncode == 0 else ""

    if script_path in existing:
        if not args.overwrite:
            print(f"Crontab entry already exists for {script_path}")
            return 0
        # Remove the old entry (and its comment header) before writing the new one
        lines = existing.splitlines()
        cleaned = []
        for i, line in enumerate(lines):
            if script_path in line:
                # Also drop the preceding comment header if it's ours
                if cleaned and cleaned[-1].startswith("# media-sorter —"):
                    cleaned.pop()
                continue
            cleaned.append(line)
        existing = "\n".join(cleaned) + "\n"
        print(f"Replacing existing crontab entry for {script_path}")

    new_crontab = existing.rstrip("\n") + ("\n" if existing.strip() else "") + entry + "\n"
    proc = subprocess.run(["crontab", "-"], input=new_crontab, text=True)
    if proc.returncode == 0:
        print(f"Installed crontab entry:\n  {entry}")
        return 0
    else:
        print("Failed to install crontab entry.", file=sys.stderr)
        return 1


def print_plan_table(plan: "MovePlan", dest_dir: Path, skipped: int, dry_run: bool) -> None:
    """Print a plain ASCII summary table of the planned moves."""
    label = "DRY RUN PLAN" if dry_run else "MOVE PLAN"
    col_name = 50
    col_dest = max((len(f"{dest_dir.name}/{mt}") for _, mt in plan), default=12)
    arrow = "  ->  "
    sep = "-" * (col_name + col_dest + len(arrow))

    print(f"\n  {label}")
    print(f"  {sep}")
    print(f"  {'Item':<{col_name}}{arrow}{'Destination':<{col_dest}}")
    print(f"  {sep}")
    for src, media_type in plan:
        name = src.name if len(src.name) <= col_name else src.name[:col_name - 5] + "[...]"
        print(f"  {name:<{col_name}}{arrow}{dest_dir.name}/{media_type}")
    print(f"  {sep}")
    print(f"  To move : {len(plan)}")
    print(f"  Skipped : {skipped}")
    print()


def print_result_table(moved: int, skipped: int, errors: int) -> None:
    """Print a plain ASCII result summary."""
    sep = "-" * 24
    print(f"\n  RESULT")
    print(f"  {sep}")
    print(f"  {'Moved':<10}  {moved}")
    print(f"  {'Skipped':<10}  {skipped}")
    print(f"  {'Errors':<10}  {errors}")
    print(f"  {sep}")
    print()


def main() -> int:
    args = build_parser().parse_args()

    if args.install_cron:
        return install_cron(os.path.abspath(__file__), args)

    log_level = logging.DEBUG if (args.verbose or args.debug) else logging.INFO
    date_suffix = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = str(Path(args.log_dir) / f"media-sorter-{date_suffix}.log")
    initialize_logger(log_level=log_level, log_filename=log_filename, scope="media_sorter")
    cleanup_old_logs(args.log_dir)

    exclusion_patterns = load_exclusions(args.excludes, args.exclude_from)
    if exclusion_patterns:
        logger.debug("Loaded %d exclusion pattern(s).", len(exclusion_patterns))

    source_dir = Path(args.source)
    dest_dir = Path(args.destination)

    # Ensure standard media subdirectories exist under destination
    for subdir in MEDIA_SUBDIRS:
        d = dest_dir / subdir
        if not d.exists():
            logger.info("Creating missing media directory: %s", d)
            d.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        logger.info("DRY RUN — pass --no-dry-run to move files")

    logger.info("Source:      %s", source_dir)
    logger.info("Destination: %s", dest_dir)

    tmdb_key = resolve_tmdb_key(args.tmdb_key)
    if tmdb_key:
        logger.debug("TMDb primary lookup enabled.")
    else:
        logger.debug(
            "No TMDb key — falling back to regex detection only.\n"
            "  To enable TMDb lookup, do any of:\n"
            "    1. echo 'YOUR_KEY' > ~/.tmdb.key\n"
            "    2. export TMDB_API_KEY=YOUR_KEY\n"
            "    3. Pass --tmdb-key YOUR_KEY\n"
            "  Get a free key at: themoviedb.org/settings/api"
        )

    plan, skipped = build_plan(
        downloads_dir=source_dir,
        exclusion_patterns=exclusion_patterns,
        debug=args.debug,
        tmdb_key=tmdb_key,
        logger=logger,
    )

    if not plan:
        logger.info("Nothing to move (skipped: %d).", skipped)
        return 0

    print_plan_table(plan, dest_dir, skipped, dry_run=args.dry_run)

    if args.dry_run:
        logger.info("Dry-run complete — would move: %d  skipped: %d", len(plan), skipped)
        return 0

    # Confirm before executing real moves
    if not args.no_confirm:
        answer = input("Proceed? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            logger.info("Aborted by user.")
            return 0

    moved, errors = execute_plan(
        plan=plan,
        dest_dir=dest_dir,
        overwrite=args.overwrite,
        logger=logger,
    )

    print_result_table(moved, skipped, errors)
    logger.info("Finished — moved: %d  skipped: %d  errors: %d", moved, skipped, errors)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
