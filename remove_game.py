import os
import shutil
from pathlib import Path
from add_game_to_webpage import list_all_games, sync_games_with_webpage

def remove_game():
    """Interactively removes a game and updates the webpage."""

    # Get the list of games
    games = list_all_games()

    if not games:
        print("No games found to remove.")
        return

    # Display the list of games
    print("Available games:")
    for i, game in enumerate(games, 1):
        print(f"  {i}. {game['name']}")

    # Prompt user for which game to remove
    try:
        choice = int(input("Enter the number of the game to remove (or 0 to cancel): "))
        if choice == 0:
            print("Operation cancelled.")
            return
        if not 1 <= choice <= len(games):
            print("Invalid number. Please try again.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    # Get the selected game
    selected_game = games[choice - 1]
    game_folder_path = Path("games") / selected_game['folder']

    # Confirm deletion
    confirm = input(f"Are you sure you want to delete '{selected_game['name']}'? This cannot be undone. (y/n): ")
    if confirm.lower() != 'y':
        print("Deletion cancelled.")
        return

    # Delete the game folder
    if game_folder_path.exists() and game_folder_path.is_dir():
        try:
            shutil.rmtree(game_folder_path)
            print(f"Successfully deleted game folder: {game_folder_path}")
        except OSError as e:
            print(f"Error deleting game folder: {e}")
            return
    else:
        print(f"Game folder not found: {game_folder_path}")

    # Sync the webpage
    print("\nSyncing webpage to remove the deleted game...")
    try:
        games_count = sync_games_with_webpage()
        print(f"✨ Webpage sync complete! {games_count} game(s) are now displayed.")
    except Exception as e:
        print(f"An error occurred during webpage sync: {e}")

if __name__ == "__main__":
    remove_game()