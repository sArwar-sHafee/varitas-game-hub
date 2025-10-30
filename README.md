# Varitas Game Hub

A lightweight collection of handcrafted browser games with automatic daily generation. Each game is a single-file HTML5 Canvas experience with programmatic audio and simple controls. Play locally or host with GitHub Pages.

Live demo: https://sarwar-shafee.github.io/varitas-game-hub/  
Open the site locally: [index.html](index.html)

---

## Highlights

- Dozens of small, polished HTML5 games in the `games/` folder ([games/](games/))
- Automatic daily game generation using AI via [generate_game.py](generate_game.py)
- Webpage sync helper: [`sync_games_with_webpage()`](add_game_to_webpage.py) in [add_game_to_webpage.py](add_game_to_webpage.py)
- CI automation and scheduled generation under [.github/workflows/](.github/workflows/)
- Setup and troubleshooting guidance in [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)

---

## Quick Start (Local)

1. Install dependencies:
```sh
pip install -r requirements.txt
```

2. Generate a new game locally:
```sh
python generate_game.py
```
This runs the [`generate_game()`](generate_game.py) logic and saves a new folder under `games/`.

3. Sync games into the hub page:
```sh
python add_game_to_webpage.py
```
This will update the root [index.html](index.html) listing via [`sync_games_with_webpage()`](add_game_to_webpage.py).

4. Run daily tasks manually:
```sh
./run_daily_tasks.sh
# or
bash run_daily_tasks.sh
```
The script simply runs `python generate_game.py` (see [run_daily_tasks.sh](run_daily_tasks.sh)).

---

## Project Layout

- index.html — The games hub page that lists and links to games. ([index.html](index.html))
- games/ — Each game lives in its own folder under this directory. ([games/](games/))
- generate_game.py — AI-driven game generator and saver. ([generate_game.py](generate_game.py))
- add_game_to_webpage.py — Updates `index.html` to include new games. ([add_game_to_webpage.py](add_game_to_webpage.py))
- run_daily_tasks.sh — Simple wrapper to run generation. ([run_daily_tasks.sh](run_daily_tasks.sh))
- SETUP_INSTRUCTIONS.md — CI, secrets, and deployment instructions. ([SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md))
- .github/workflows/ — GitHub Actions workflows for scheduled generation and cleanup. ([.github/workflows/](.github/workflows/))

---

## CI / Deployment

- The repo contains GitHub Actions workflows to:
  - Generate games on a schedule
  - Keep only the most recent games
  - Deploy the site to GitHub Pages

See [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for configuring:
- `GEMINI_API_KEY` secret
- GitHub Pages settings
- Workflow schedule customization

---

## Contributing

- Add new hand-crafted games by creating a folder under `games/` with an `index.html` and `cover.png` (or let the generator produce both).
- If you modify generator behavior, update tests and run locally before pushing.
- Follow the style used in existing games for sound (Web Audio API), canvas sizing, and responsiveness.

---

## Troubleshooting

- Games not appearing after generation? Run:
```sh
python add_game_to_webpage.py
```
- CI issues or API problems? Consult [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) and check the Actions logs under the repository's **Actions** tab.
- For local audio issues, ensure the browser allows AudioContext playback after a user gesture.

---

## License & Credits

- Content and code in this repo are provided "as-is". Add a LICENSE file as desired.
- Generator uses the configured Gemini API key (see [generate_game.py](generate_game.py)). Keep API keys out of the repo and use GitHub Secrets.

---

If you want, I can:
- Create a shorter landing README for the GitHub repo front page
- Add a CONTRIBUTING.md or LICENSE file
- Generate a badge block for CI status and GitHub Pages

```// filepath: /workspaces/varitas-game-hub/README.md
// ...existing code...

# Varitas Game Hub

A lightweight collection of handcrafted browser games with automatic daily generation. Each game is a single-file HTML5 Canvas experience with programmatic audio and simple controls. Play locally or host with GitHub Pages.

Live demo: https://sarwar-shafee.github.io/varitas-game-hub/  
Open the site locally: [index.html](index.html)

---

## Highlights

- Dozens of small, polished HTML5 games in the `games/` folder ([games/](games/))
- Automatic daily game generation using AI via [generate_game.py](generate_game.py)
- Webpage sync helper: [`sync_games_with_webpage()`](add_game_to_webpage.py) in [add_game_to_webpage.py](add_game_to_webpage.py)
- CI automation and scheduled generation under [.github/workflows/](.github/workflows/)
- Setup and troubleshooting guidance in [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)

---

## Quick Start (Local)

1. Install dependencies:
```sh
pip install -r requirements.txt
```

2. Generate a new game locally:
```sh
python generate_game.py
```
This runs the [`generate_game()`](generate_game.py) logic and saves a new folder under `games/`.

3. Sync games into the hub page:
```sh
python add_game_to_webpage.py
```
This will update the root [index.html](index.html) listing via [`sync_games_with_webpage()`](add_game_to_webpage.py).

4. Run daily tasks manually:
```sh
./run_daily_tasks.sh
# or
bash run_daily_tasks.sh
```
The script simply runs `python generate_game.py` (see [run_daily_tasks.sh](run_daily_tasks.sh)).

---

## Project Layout

- index.html — The games hub page that lists and links to games. ([index.html](index.html))
- games/ — Each game lives in its own folder under this directory. ([games/](games/))
- generate_game.py — AI-driven game generator and saver. ([generate_game.py](generate_game.py))
- add_game_to_webpage.py — Updates `index.html` to include new games. ([add_game_to_webpage.py](add_game_to_webpage.py))
- run_daily_tasks.sh — Simple wrapper to run generation. ([run_daily_tasks.sh](run_daily_tasks.sh))
- SETUP_INSTRUCTIONS.md — CI, secrets, and deployment instructions. ([SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md))
- .github/workflows/ — GitHub Actions workflows for scheduled generation and cleanup. ([.github/workflows/](.github/workflows/))

---

## CI / Deployment

- The repo contains GitHub Actions workflows to:
  - Generate games on a schedule
  - Keep only the most recent games
  - Deploy the site to GitHub Pages

See [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for configuring:
- `GEMINI_API_KEY` secret
- GitHub Pages settings
- Workflow schedule customization

---

## Contributing

- Add new hand-crafted games by creating a folder under `games/` with an `index.html` and `cover.png` (or let the generator produce both).
- If you modify generator behavior, update tests and run locally before pushing.
- Follow the style used in existing games for sound (Web Audio API), canvas sizing, and responsiveness.

---

## Troubleshooting

- Games not appearing after generation? Run:
```sh
python add_game_to_webpage.py
```
- CI issues or API problems? Consult [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) and check the Actions logs under the repository's **Actions** tab.
- For local audio issues, ensure the browser allows AudioContext playback after a user gesture.

## Follow the link to start:

https://sarwar-shafee.github.io/varitas-game-hub/
