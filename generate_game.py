import os
import json
import random
from pathlib import Path
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
import colorsys
import requests
from io import BytesIO
import os

# Configure Gemini API
API_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=API_KEY)

# Game types to randomly choose from
GAME_TYPES = [
    "2D platformer",
    "puzzle game",
    "memory card game",
    "snake game",
    "breakout/brick breaker",
    "tic-tac-toe with AI",
    "space shooter",
    "maze game",
    "whack-a-mole",
    "simon says memory game",
    "color matching game",
    "number guessing game",
    "rock paper scissors",
    "bubble shooter",
    "word scramble game"
]

def generate_cover_image_with_ai(game_name, game_type, game_description, output_path, model):
    """Generate a cover image using Gemini's Imagen model"""
    try:
        # Create a detailed prompt for image generation
        image_prompt = f"""Create a colorful, vibrant game cover image for a {game_type} called "{game_name}".
        {game_description}

        The image should:
        - Be bright, colorful and appealing to gamers
        - Show game-related elements and characters
        - Have a professional game cover art style
        - Include visual elements that represent the gameplay
        - Be suitable for all ages
        - Have a fun, playful aesthetic

        Style: Digital art, game cover art, vibrant colors, high quality illustration"""

        print(f"Generating AI cover image for {game_name}...")

        # Try to use Imagen 3 for image generation
        try:
            imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")
            response = imagen.generate_images(
                prompt=image_prompt,
                number_of_images=1,
                aspect_ratio="16:9",
                safety_filter_level="block_some",
                person_generation="allow_adult"
            )

            if response.images:
                # Save the generated image
                response.images[0].save(output_path)
                print(f"AI-generated cover image saved: {output_path}")
                return True
        except:
            # If Imagen fails, try using the text model to create an SVG
            pass

        # Fallback: Ask Gemini to create SVG art
        svg_prompt = f"""Create a simple SVG image code for a game cover of "{game_name}" - a {game_type}.
        The SVG should be 800x600 pixels and include:
        - Colorful gradient background
        - Simple geometric shapes representing game elements
        - The game title "{game_name}"
        - Fun, playful design

        Return ONLY the SVG code, starting with <svg and ending with </svg>."""

        svg_response = model.generate_content(svg_prompt)
        svg_code = svg_response.text

        # Extract SVG code
        if "<svg" in svg_code:
            svg_start = svg_code.index("<svg")
            svg_end = svg_code.index("</svg>") + 6
            svg_code = svg_code[svg_start:svg_end]

            # Convert SVG to PNG using a temporary file
            from cairosvg import svg2png
            svg2png(bytestring=svg_code.encode('utf-8'), write_to=str(output_path))
            print(f"SVG-based cover image saved: {output_path}")
            return True

    except Exception as e:
        print(f"AI image generation failed: {e}")
        print("Falling back to programmatic image generation...")

    # Fallback to programmatic generation
    return False

def generate_cover_image_fallback(game_name, game_type, output_path):
    """Fallback: Generate a simple programmatic cover image"""
    width, height = 800, 600
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    # Generate vibrant colors based on game type
    game_type_colors = {
        "platformer": [(255, 100, 100), (255, 200, 100)],
        "puzzle": [(100, 255, 100), (100, 255, 200)],
        "snake": [(100, 100, 255), (200, 100, 255)],
        "shooter": [(255, 50, 50), (255, 150, 50)],
        "memory": [(255, 200, 50), (255, 255, 150)],
        "maze": [(150, 100, 200), (200, 150, 255)],
        "racing": [(255, 100, 0), (255, 200, 0)],
    }

    # Get colors based on game type
    default_colors = [(100, 150, 255), (200, 100, 255)]
    for key in game_type_colors:
        if key in game_type.lower():
            colors = game_type_colors[key]
            break
    else:
        colors = default_colors

    rgb1, rgb2 = colors

    # Create gradient background
    for y in range(height):
        ratio = y / height
        r = int(rgb1[0] * (1 - ratio) + rgb2[0] * ratio)
        g = int(rgb1[1] * (1 - ratio) + rgb2[1] * ratio)
        b = int(rgb1[2] * (1 - ratio) + rgb2[2] * ratio)
        draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))

    # Add game-themed decorative elements
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    # Add circles for a playful look
    for i in range(8):
        x = random.randint(100, width - 100)
        y = random.randint(100, height - 100)
        size = random.randint(30, 80)
        alpha = random.randint(30, 100)
        color = (*rgb1, alpha) if i % 2 == 0 else (*rgb2, alpha)
        overlay_draw.ellipse([x - size, y - size, x + size, y + size], fill=color)

    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

    # Add text
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    except:
        try:
            # Try Windows fonts
            font_title = ImageFont.truetype("arial.ttf", 60)
            font_subtitle = ImageFont.truetype("arial.ttf", 30)
        except:
            # Ultimate fallback
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()

    # Draw game name
    draw = ImageDraw.Draw(img)
    text = game_name.upper()

    # Get text size
    bbox = draw.textbbox((0, 0), text, font=font_title)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2 - 30

    # Add shadow and text
    draw.text((text_x + 3, text_y + 3), text, fill=(0, 0, 0), font=font_title)
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font_title)

    # Draw game type
    subtext = f"~ {game_type} ~"
    bbox = draw.textbbox((0, 0), subtext, font=font_subtitle)
    subtext_width = bbox[2] - bbox[0]
    subtext_x = (width - subtext_width) // 2
    subtext_y = text_y + text_height + 20

    draw.text((subtext_x + 2, subtext_y + 2), subtext, fill=(0, 0, 0), font=font_subtitle)
    draw.text((subtext_x, subtext_y), subtext, fill=(220, 220, 220), font=font_subtitle)

    # Save image
    img.save(output_path, quality=95)
    print(f"Programmatic cover image saved: {output_path}")

def generate_game():
    """Generate a complete game using Gemini API"""

    # Randomly select a game type
    game_type = random.choice(GAME_TYPES)
    print(f"Generating {game_type}...")

    # Initialize Gemini model
    model = genai.GenerativeModel('gemini-2.5-pro')

    # Generate game name
    name_prompt = f"""Generate a creative, catchy, and unique name for a {game_type} game.
    The name should be:
    - 2-3 words maximum
    - Fun and memorable
    - Related to the game type
    - Suitable for all ages
    Just return the name, nothing else."""

    name_response = model.generate_content(name_prompt)
    game_name = name_response.text.strip().replace('"', '').replace("'", "").replace(":", "").replace("/", "-")
    print(f"Game name: {game_name}")

    # Create folder for the game with duplicate name handling
    base_folder_name = game_name.replace(" ", "_").lower()
    folder_name = base_folder_name
    game_folder = Path(f"games/{folder_name}")

    # Check if folder already exists and append number if needed
    counter = 2
    while game_folder.exists():
        folder_name = f"{base_folder_name}_{counter}"
        game_folder = Path(f"games/{folder_name}")
        counter += 1

    # Create the unique folder
    game_folder.mkdir(parents=True, exist_ok=False)

    # Update game name if it was duplicated
    if folder_name != base_folder_name:
        suffix_num = folder_name.split('_')[-1]
        game_name = f"{game_name} {suffix_num}"
        print(f"⚠️  Duplicate name detected! Renamed to: {game_name}")

    # Generate game code
    code_prompt = f"""Create a complete, playable {game_type} game called "{game_name}" using HTML5 Canvas and JavaScript.

Requirements:
1. Single HTML file with embedded CSS and JavaScript
2. Use HTML5 Canvas for graphics
3. Include keyboard/mouse controls with on-screen instructions
4. Add score tracking where applicable
5. Include game over and restart functionality
6. Use modern JavaScript (ES6+)
7. Add nice visual effects and smooth animations
8. Make it colorful and visually appealing
9. Include sound effects using Web Audio API or HTML5 Audio (create simple programmatic sounds)
10. Make it responsive to different screen sizes

The game should be:
- Fully functional and bug-free
- Fun and engaging
- Polished with good UI/UX
- Complete with start screen, game play, and game over screen

Generate the COMPLETE HTML file with ALL code. Do not use any external dependencies or images.
Use CSS gradients, Canvas drawing, and emoji for all graphics.
Make sure the game is immediately playable when opened in a browser."""

    code_response = model.generate_content(code_prompt)
    game_code = code_response.text

    # Extract HTML code from response (in case it's wrapped in markdown)
    if "```html" in game_code:
        game_code = game_code.split("```html")[1].split("```")[0]
    elif "```" in game_code:
        game_code = game_code.split("```")[1].split("```")[0]

    # Save game HTML file
    game_file = game_folder / "index.html"
    with open(game_file, 'w', encoding='utf-8') as f:
        f.write(game_code.strip())
    print(f"Game code saved: {game_file}")

    # Validate the generated game code
    print("\n🔍 Validating game code...")
    validation_prompt = f"""Please review this HTML game code for "{game_name}" and check if it will work correctly:

{game_code}

Please analyze and fix any issues found. Return the corrected HTML code that:
1. Has no JavaScript syntax errors
2. Has proper event listeners and game initialization
3. Has all required functions defined
4. Has proper HTML structure
5. Will actually run when opened in a browser

Return ONLY the complete, corrected HTML code without any markdown formatting or explanations."""

    validation_response = model.generate_content(validation_prompt)
    validated_code = validation_response.text

    # Extract HTML code from response (in case it's wrapped in markdown)
    if "```html" in validated_code:
        validated_code = validated_code.split("```html")[1].split("```")[0]
    elif "```" in validated_code:
        validated_code = validated_code.split("```")[1].split("```")[0]

    # Save the validated game HTML file
    with open(game_file, 'w', encoding='utf-8') as f:
        f.write(validated_code.strip())
    print(f"✅ Game code validated and saved: {game_file}")

    # Generate game description for cover image
    desc_prompt = f"""Write a brief, exciting description (2 sentences max) for a {game_type} called "{game_name}".
    Focus on the gameplay and what makes it fun. Be creative and engaging."""

    desc_response = model.generate_content(desc_prompt)
    game_description = desc_response.text.strip()

    # Generate cover image
    cover_path = game_folder / "cover.png"

    # Try AI generation first
    if not generate_cover_image_with_ai(game_name, game_type, game_description, cover_path, model):
        # Fallback to programmatic generation
        generate_cover_image_fallback(game_name, game_type, cover_path)

    # Save game metadata
    metadata = {
        "name": game_name,
        "type": game_type,
        "folder": folder_name,
        "description": game_description,
        "cover": "cover.png",
        "main_file": "index.html"
    }

    metadata_file = game_folder / "metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata saved: {metadata_file}")

    print(f"\n✅ Game '{game_name}' generated successfully!")
    print(f"📁 Location: {game_folder}")
    return metadata

if __name__ == "__main__":
    game_info = generate_game()
    print("\nGame generation complete!")
    print("Run 'add_game_to_webpage.py' to add this game to your website.")