import argparse
import json
import os
import re
import time
from urllib.parse import parse_qs, urlparse

import requests
from deep_translator import GoogleTranslator
from langdetect import detect


def is_english(text):
    # This doesn't work, FIX ME
    return detect(text) == "en"


def translate_to_english(text):
    print("Translating text, please wait...")
    translator = GoogleTranslator(source="auto", target="en")
    lines = text.split("\n")
    translated_lines = []

    total_count = 0
    for line in lines:
        total_count += 1
        if not line.strip():  # Skip empty lines
            continue
        try:
            # Add a small delay to avoid rate limiting
            time.sleep(0.5)
            print(f"Translating line: {total_count}")
            translated_line = translator.translate(line)
            translated_lines.append(translated_line)
        except Exception as e:
            print(f"Error translating line: {line}")
            print(f"Error: {str(e)}")
            translated_lines.append(line)  # Keep original if translation fails

    return "\n".join(translated_lines)


def get_video_info(url):
    """
    Fetch video info from url
    """

    try:
        # Add headers to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Fetch the video page
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html_content = response.text

        # Try to find the initial data JSON
        data_matches = [
            re.search(r"var ytInitialData = ({.*?});", html_content),
            re.search(r"ytInitialData\s*=\s*({.*?});", html_content),
        ]

        data_match = next((m for m in data_matches if m is not None), None)
        if not data_match:
            return "Could not find video data in the page."

        data = json.loads(data_match.group(1))

        # Write data to ~//youtube-recipe-extract.json
        home = os.path.expanduser("~")
        with open(f"{home}/youtube-recipe-extract.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Data written to {home}/youtube-recipe-extract.json")

        # Navigate through the JSON structure more carefully
        video_data = data["contents"]["twoColumnWatchNextResults"]["results"][
            "results"
        ]["contents"]

        # Parse list elements from video_data
        for element in video_data:
            if "videoPrimaryInfoRenderer" in element:
                title = element["videoPrimaryInfoRenderer"]["title"]["runs"][0]["text"]
            elif "videoSecondaryInfoRenderer" in element:
                description = element["videoSecondaryInfoRenderer"][
                    "attributedDescription"
                ]["content"]
                channel_owner = element["videoSecondaryInfoRenderer"]["owner"][
                    "videoOwnerRenderer"
                ]["title"]["runs"][0]["text"]
                break

        # Translate?
        # if not is_english(title):
        # print("Translating title...")
        title = translate_to_english(title)
        ## if not is_english(description):
        # print("Translating description...")
        description = translate_to_english(description)

        return {"title": title, "channel": channel_owner, "description": description}

    except requests.RequestException as e:
        return f"Network error: {str(e)}"
    except Exception as e:
        raise


def main():
    parser = argparse.ArgumentParser(description="Extract YouTube video information")
    parser.add_argument("url", type=str, help="YouTube video URL")
    parser.add_argument("-o", "--output", type=str, help="Output file path (optional)")

    args = parser.parse_args()

    info = get_video_info(args.url)

    if isinstance(info, str):  # Error occurred
        print(info)
        return

    output = f"Title: {info['title']}\n\n"
    output += f"Channel: {info['channel']}\n\n"
    output += f"Description:\n{info['description']}\n\n"

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Information saved to {args.output}")
        except Exception as e:
            print(f"Error saving to file: {str(e)}")
    else:
        print(output)


if __name__ == "__main__":
    main()
