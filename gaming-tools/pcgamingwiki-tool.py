#!/usr/bin/env python
# Sample page with all fields: https://www.pcgamingwiki.com/w/api.php?action=parse&format=jsonfm&pageid=146683&prop=wikitext

import requests
import json
import argparse
import re

from bs4 import BeautifulSoup

def scrape_save_game_location(game_page_name):
    """
    Scrapes the save game location from the PCGamingWiki page for the specified game.
    There is no cargo table that seems to hold this: https://www.pcgamingwiki.com/wiki/Special:CargoTables
    """

    url = f'https://www.pcgamingwiki.com/wiki/{game_page_name}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the "Save_game_data_location" section
        save_game_location_section = soup.find(id="Save_game_data_location")
        if save_game_location_section:
            save_locations = {}
            # Find the closest table following the "Save game data location" header
            table = save_game_location_section.find_next('table')
            if table:
                rows = table.find_all('tr')
                rows = table.find_all('tr')[1:]  # Skip the header row
                for row in rows:
                    system = row.find('th', class_='table-gamedata-body-system').text.strip()
                    location = row.find('td', class_='table-gamedata-body-location').text.strip()

                    # Remove [Note N] from the location
                    location = re.sub(r'\[Note \d+\]', '', location).strip()
                    save_locations[system] = location

            return save_locations

    return {"error": "Save game locations not found."}

def fetch_game_data_by_steam_appid(steam_appid=None, game_name=None):
    """
    Fetches game data from PCGamingWiki's Cargo API using the Steam AppID or Game Name,
    including data from the Infobox_game, Video, and Cloud tables,
    and organizes Cloud fields into a separate 'cloud_providers' section.
    """
    # Base URL for the MediaWiki API on PCGamingWiki
    api_url = 'https://www.pcgamingwiki.com/w/api.php'

    # Build the "where" condition based on Steam AppID or Game Name
    if steam_appid:
        where_clause = f'Infobox_game.Steam_AppID HOLDS "{steam_appid}"'
    elif game_name:
        where_clause = f'Infobox_game._pageName="{game_name}"'
    else:
        print("You must provide either a Steam App ID or Game Name.")
        return

    # Define the parameters for the cargoquery
    params = {
        'action': 'cargoquery',
        'format': 'json',
        'tables': 'Infobox_game,Video,Cloud',  # Targeting Infobox_game, Video, and Cloud tables
        'fields': 'Infobox_game._pageName=Page,Infobox_game.Developers,Infobox_game.Released,Infobox_game.Cover_URL,Video.4K_Ultra_HD,Video.HDR,Video.Ultrawidescreen,Cloud.Steam=Steam,Cloud.GOG_Galaxy=GOG_Galaxy,Cloud.OneDrive',  # Select specific fields and rename Cloud.Steam and Cloud.GOG_Galaxy
        'join_on': 'Infobox_game._pageID=Video._pageID,Infobox_game._pageName=Cloud._pageName',  # Joining on _pageID for Video and _pageName for Cloud
        'where': where_clause,  # Filtering by Steam AppID or Game Name
        'formatversion': '2'  # Version 2 for better JSON formatting
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()

        if data and 'cargoquery' in data and len(data['cargoquery']) > 0:
            title = data['cargoquery'][0]['title']
            game_page_name = title['Page']
            game_details = {
                "Page": game_page_name,
                "Developers": title.get('Developers', 'Unknown'),
                "Released": title.get('Released', 'Unknown'),
                "Cover_URL": title.get('Cover_URL', 'Unknown'),
                "4K_Ultra_HD": title.get('4K_Ultra_HD', 'Unknown'),
                "HDR": title.get('HDR', 'Unknown'),
                "Ultrawidescreen": title.get('Ultrawidescreen', 'Unknown'),
                "cloud_providers": {
                    "Steam": title.get('Steam', 'Unknown'),
                    "GOG_Galaxy": title.get('GOG_Galaxy', 'Unknown'),
                    "OneDrive": title.get('OneDrive', 'Unknown')
                }
            }

            # Scrape the save game location after resolving the game name
            save_game_location = scrape_save_game_location(game_page_name)
            game_details['save_game_location'] = save_game_location

            # Pretty-print the final game details
            print(json.dumps(game_details, indent=4))
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Fetch game data from PCGamingWiki.")

    # Add arguments for Steam App ID and Game Name
    parser.add_argument('-s', '--steam-app-id', type=str, help="The Steam App ID of the game.")
    parser.add_argument('-g', '--game-name', type=str, help="The name of the game.")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Fetch game data using either Steam App ID or Game Name
    fetch_game_data_by_steam_appid(steam_appid=args.steam_app_id, game_name=args.game_name)

if __name__ == "__main__":
    main()

