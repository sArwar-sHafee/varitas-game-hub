import os
import json
from pathlib import Path
from bs4 import BeautifulSoup
import shutil

def get_latest_game():
    """Find the most recently created game folder"""
    games_dir = Path("games")
    if not games_dir.exists():
        print("No games directory found. Please generate a game first.")
        return None

    # Get all game folders with metadata
    game_folders = []
    for folder in games_dir.iterdir():
        if folder.is_dir():
            metadata_file = folder / "metadata.json"
            if metadata_file.exists():
                game_folders.append(folder)

    if not game_folders:
        print("No games found. Please generate a game first.")
        return None

    # Get the most recent game
    latest_game = max(game_folders, key=lambda x: x.stat().st_mtime)
    return latest_game

def add_game_to_webpage(game_folder=None):
    """Add a game to the webpage"""

    if game_folder is None:
        game_folder = get_latest_game()
        if game_folder is None:
            return False

    # Load game metadata
    metadata_file = game_folder / "metadata.json"
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)

    print(f"Adding game: {metadata['name']}")

    # Read the current HTML file
    html_file = Path("index.html")
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Find the games grid
    games_grid = soup.find('div', class_='games-grid')
    if not games_grid:
        print("Error: Could not find games grid in HTML")
        return False

    # Check if game already exists
    existing_games = games_grid.find_all('div', class_='game-card')
    for game in existing_games:
        title_elem = game.find('h2', class_='game-title')
        if title_elem and metadata['name'] in title_elem.text:
            print(f"Game '{metadata['name']}' already exists in the webpage")
            return False

    # Create new game card HTML
    game_card_html = f"""
    <div class="game-card">
        <a href="games/{metadata['folder']}/index.html" style="text-decoration: none;">
            <div class="game-image" style="background-image: url('games/{metadata['folder']}/cover.png'); background-size: cover; background-position: center;">
            </div>
            <div class="game-info">
                <h2 class="game-title">{metadata['name']}</h2>
                <p class="game-description">{metadata['description']}</p>
                <span class="play-button">Play Now</span>
            </div>
        </a>
    </div>
    """

    # Parse the new game card HTML
    new_game_card = BeautifulSoup(game_card_html, 'html.parser')

    # Find the first placeholder game card with "Game" in the title
    placeholder_found = False
    for i, game_card in enumerate(existing_games):
        game_image = game_card.find('div', class_='game-image')
        if game_image and game_image.text and 'Game' in game_image.text.strip():
            # Replace this placeholder with the new game
            game_card.replace_with(new_game_card)
            placeholder_found = True
            print(f"Replaced placeholder game {i+1} with '{metadata['name']}'")
            break

    # If no placeholder found, append the new game
    if not placeholder_found:
        games_grid.append(new_game_card)
        print(f"Added '{metadata['name']}' to the games grid")

    # Update the CSS to handle background images properly
    style_tag = soup.find('style')
    if not style_tag:
        # If using external CSS, we need to update the CSS file
        css_file = Path("styles.css")
        if css_file.exists():
            with open(css_file, 'r') as f:
                css_content = f.read()

            # Add background-image support if not already present
            if "background-image:" not in css_content:
                additional_css = """
.game-image[style*="background-image"] {
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
}

.game-image[style*="background-image"]::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.1) 100%);
    pointer-events: none;
}
"""
                with open(css_file, 'a') as f:
                    f.write(additional_css)
                print("Updated CSS file with background image support")

    # Save the updated HTML
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))

    print(f"✅ Successfully added '{metadata['name']}' to the webpage!")
    print(f"🎮 Game URL: games/{metadata['folder']}/index.html")
    return True

def list_all_games():
    """List all available games"""
    games_dir = Path("games")
    if not games_dir.exists():
        print("No games found.")
        return []

    games = []
    for folder in games_dir.iterdir():
        if folder.is_dir():
            metadata_file = folder / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    games.append(metadata)

    return games

def sync_games_with_webpage():
    """Sync the webpage with the games folder - add new games and remove deleted ones"""
    games = list_all_games()

    # Read the current HTML file
    html_file = Path("index.html")
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Find the games grid
    games_grid = soup.find('div', class_='games-grid')
    if not games_grid:
        print("Error: Could not find games grid in HTML")
        return False

    # Get all existing game cards
    existing_cards = games_grid.find_all('div', class_='game-card')

    # Clear all game cards (we'll rebuild from games folder)
    for card in existing_cards:
        card.decompose()

    # Add placeholder cards first
    placeholder_count = 6  # Number of placeholder cards to maintain
    games_added = 0

    # Add all games from the games folder
    for game in games:
        game_card_html = f"""
        <div class="game-card">
            <a href="games/{game['folder']}/index.html" style="text-decoration: none;">
                <div class="game-image" style="background-image: url('games/{game['folder']}/cover.png'); background-size: cover; background-position: center;">
                </div>
                <div class="game-info">
                    <h2 class="game-title">{game['name']}</h2>
                    <p class="game-description">{game['description']}</p>
                    <span class="play-button">Play Now</span>
                </div>
            </a>
        </div>
        """
        new_game_card = BeautifulSoup(game_card_html, 'html.parser')
        games_grid.append(new_game_card)
        games_added += 1
        print(f"✅ Added: {game['name']}")

    # Add placeholder cards to fill remaining slots
    for i in range(games_added, placeholder_count):
        placeholder_html = f"""
        <div class="game-card">
            <a href="#" style="text-decoration: none;">
                <div class="game-image">
                    Game {i + 1}
                </div>
                <div class="game-info">
                    <h2 class="game-title">Coming Soon</h2>
                    <p class="game-description">New game will be added here soon!</p>
                    <span class="play-button">Play Now</span>
                </div>
            </a>
        </div>
        """
        placeholder_card = BeautifulSoup(placeholder_html, 'html.parser')
        games_grid.append(placeholder_card)

    # Save the updated HTML
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))

    return games_added

if __name__ == "__main__":
    print("=" * 50)
    print("SYNC GAMES WITH WEBPAGE")
    print("=" * 50)

    # List current games
    games = list_all_games()

    print(f"\n📂 Games in folder: {len(games)}")
    if games:
        for i, game in enumerate(games, 1):
            print(f"  {i}. {game['name']} - {game['type']}")
    else:
        print("  No games found in games folder")

    print("\n🔄 Syncing webpage with games folder...")
    print("This will:")
    print("  • Remove games that no longer exist in the folder")
    print("  • Add new games from the folder")
    print("  • Maintain placeholder slots for future games")
    print()

    games_count = sync_games_with_webpage()

    if games_count > 0:
        print(f"\n✨ Sync complete! {games_count} game(s) on webpage")
    else:
        print("\n✨ Sync complete! Webpage now shows placeholder cards only")

    print("🌐 Open index.html to see your updated gaming hub.")