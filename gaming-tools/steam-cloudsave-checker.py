#!/usr/bin/env python
# Sample page with all fields: https://www.pcgamingwiki.com/w/api.php?action=parse&format=jsonfm&pageid=146683&prop=wikitext

import requests
import json
import argparse

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

    # Send the request to the MediaWiki API
    response = requests.get(api_url, params=params)

    # Check if the response was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # If there are results, restructure the output
        if data and 'cargoquery' in data and len(data['cargoquery']) > 0:
            for entry in data['cargoquery']:
                title = entry['title']

                # Extract cloud-related fields and organize them under 'cloud_providers'
                cloud_providers = {
                    'Steam': title.pop('Steam', 'Unknown'),
                    'GOG_Galaxy': title.pop('GOG_Galaxy', 'Unknown'),
                    'OneDrive': title.pop('OneDrive', 'Unknown')
                }

                # Add the 'cloud_providers' key to the output
                title['cloud_providers'] = cloud_providers

        # Pretty-print the reorganized JSON response
        print(json.dumps(data, indent=4))
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

