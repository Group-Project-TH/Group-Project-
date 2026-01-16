import asyncio
import json
from playwright.async_api import async_playwright
import re

async def scrape_and_save_player_ids():
    """
    Scrapes player IDs directly from the RoyaleAPI leaderboard page and saves them to a JSON file.
    """
    player_ids = []
    async with async_playwright() as p:
        # Launch the browser (set headless=False to see the browser actions)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Navigate to the leaderboard page
            await page.goto('https://royaleapi.com/players/leaderboard/')
            
            # Wait for the player name table cells to be present in the DOM
            await page.wait_for_selector('td.player_leaderboard__player_name a.ui.tiny.header')
            
            # Get all the player name links
            player_links = await page.query_selector_all('td.player_leaderboard__player_name a.ui.tiny.header')
            
            print(f"Found {len(player_links)} player links. Extracting IDs...")

            for index, link in enumerate(player_links, start=1):
                try:
                    # Get the href attribute which contains the player ID
                    href = await link.get_attribute('href')
                    
                    # Extract the ID part from the href (e.g., "/player/2Q2QCYLPR" -> "2Q2QCYLPR")
                    # Using regex to capture the part after '/player/'
                    match = re.search(r'/player/([^/]+)', href)
                    if match:
                        player_id = match.group(1)
                        player_ids.append(player_id)
                        print(f"Extracted ({index}/{len(player_links)}): {player_id}")
                    else:
                        print(f"Could not extract ID from href: {href}")

                except Exception as e:
                    print(f"Error processing link {index}: {e}")
                    print(f"Exception details: {e}")
                    continue # Move to the next link even if an error occurred

        except Exception as e:
            print(f"An error occurred during the scraping process: {e}")

        finally:
            await browser.close()

    print(f"\nScraping completed. Total Player IDs collected: {len(player_ids)}")
    
    # Save the list of player IDs to a JSON file
    filename = "100top_player_ids.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(player_ids, f, indent=4) # indent for pretty printing in the file
        print(f"Player IDs successfully saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
        return None
        
    return player_ids

# Run the scraper
if __name__ == "__main__":
    player_ids = asyncio.run(scrape_and_save_player_ids())
    if player_ids:
        print("\n--- First 5 Player IDs from the list ---")
        for i, tag in enumerate(player_ids[:5], start=1):
            print(f"{i}: {tag}")
        if len(player_ids) > 5:
            print(f"... and {len(player_ids) - 5} more.")