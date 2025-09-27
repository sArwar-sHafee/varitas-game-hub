# GitHub Actions Setup Instructions

## 🚀 Setting up Automatic Daily Game Generation

Follow these steps to enable automatic game generation on your GitHub repository:

### 1. Push Code to GitHub

```bash
git add .
git commit -m "Add gaming hub with automatic game generation"
git push origin main
```

### 2. Add Gemini API Key to GitHub Secrets

1. Go to your repository on GitHub
2. Click on **Settings** (in the repository, not your profile)
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Add the following secret:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: Your Gemini API key (without quotes)
6. Click **Add secret**

### 3. Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. If prompted, enable GitHub Actions for the repository
3. You should see "Daily Game Generation" workflow

### 4. Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Under "Source", select **Deploy from a branch**
3. Choose **main** branch and **/ (root)** folder
4. Click **Save**
5. Your site will be available at: `https://[your-username].github.io/[repository-name]/`

## ⚙️ How It Works

- **Daily Generation**: Automatically generates 1 new game every day at 12:00 UTC
- **Manual Trigger**: You can manually generate 1-3 games anytime from the Actions tab
- **Auto Cleanup**: Keeps only the last 20 games to save space (runs weekly)
- **Auto Deploy**: Updates are automatically deployed to GitHub Pages

## 🎮 Manual Game Generation

### From GitHub Actions:
1. Go to the **Actions** tab
2. Click on **Daily Game Generation**
3. Click **Run workflow**
4. Select how many games to generate (1-3)
5. Click **Run workflow**

### Locally:
```bash
# Generate a game
python generate_game.py

# Update webpage
python add_game_to_webpage.py

# Push changes
git add .
git commit -m "Added new game"
git push
```

## 📝 Customization

### Change Generation Schedule

Edit `.github/workflows/daily-game-generation.yml`:

```yaml
schedule:
  - cron: '0 12 * * *'  # Current: 12:00 UTC daily
```

Common schedules:
- `'0 0 * * *'` - Midnight UTC daily
- `'0 */6 * * *'` - Every 6 hours
- `'0 12 * * 1'` - Every Monday at noon
- `'0 0 * * 0'` - Every Sunday at midnight

### Change Maximum Games

Edit the cleanup section to keep more/fewer games:
```yaml
# Keep only the 20 most recent games
```
Change `20` to your desired number.

## 🔧 Troubleshooting

### Workflow Not Running?
- Check Actions tab for any error messages
- Verify GEMINI_API_KEY is set correctly in Secrets
- Ensure GitHub Actions is enabled for the repository

### Games Not Appearing on Website?
- Check if GitHub Pages is enabled
- Wait 5-10 minutes for deployment after push
- Clear browser cache and refresh

### API Key Issues?
- Regenerate your Gemini API key if needed
- Update the secret in GitHub repository settings
- Make sure the key has proper permissions

## 📊 Monitor Usage

- Check **Actions** tab to see workflow history
- Each run shows logs and generated games
- Failed runs will show error messages

## 🎯 Best Practices

1. **Don't commit API keys** - Always use GitHub Secrets
2. **Monitor API usage** - Gemini API has rate limits
3. **Regular cleanup** - The workflow auto-removes old games weekly
4. **Test locally first** - Run scripts locally before pushing

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)