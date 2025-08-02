# 🐦 x-notifications - X Post Alert Bot 🤖

A simple Python script that monitors a specified X user's posts and sends alerts to a Discord webhook when new content is detected.

## ✨ Features

- 🔍 Monitors a X user's timeline for new posts
- 📨 Sends detailed alerts to Discord including:
  - 📝 Post text/content
  - 📊 Engagement metrics (likes, retweets, views)
  - ⏰ Timestamp
  - 🖼️ Media attachments (images/videos)
  - 🔗 Direct link to the post
- 💾 Persistent storage of seen posts to avoid duplicate alerts
- ⏱️ Automatic periodic checks (every 3 seconds)

## 📋 Requirements

- 🐍 Python 3.7+
- 🎭 Playwright (for browser automation)
- 📡 Requests (for Discord webhook communication)

## 🛠️ Installation

1. Clone this repository or download the script
2. Install the required dependencies:
   ```bash
   pip install playwright requests
   playwright install
   ```

## ⚙️ Configuration

1. Replace the `webhook_url` variable with your Discord webhook URL
2. Modify the Twitter username in the code (currently set to monitor `@janeremover`):
   - Change `'https://x.com/janeremover'` to your desired profile URL
   - Update the Discord embed title accordingly

## 🚀 Usage

Run the script with Python:
```bash
python script_name.py
```

The script will:
1. 🌐 Launch a headless browser to monitor the Twitter/X profile
2. 🔄 Check for new posts periodically
3. 📢 Send alerts to Discord when new content is detected
4. 💿 Store seen posts in `tweets.json` to avoid duplicates

To stop the script, press `Ctrl+C`.

## 🎨 Customization

You can modify:
- ⏳ The check interval by adjusting the `sleep_time` calculation
- 💬 The Discord embed appearance by editing the `embed` dictionary
- 📁 The stored tweet data format in `tweets.json`

## ℹ️ Notes

- ⚠️ X may change their API structure, which could break the script
- 👀 The script currently monitors the user's main timeline (not replies or other tabs)
- 🚦 Rate limits may apply if checking too frequently

## ⚠️ Disclaimer

This script is for educational purposes only. Make sure to comply with X's Terms of Service when using this script.

---

💡 **Tip:** For best results, run this script on a server or always-on machine to ensure continuous monitoring!  
🐛 **Found an issue?** Please report it in the project's issues section.  
🌟 **Enjoying the bot?** Give the repo a star!  

## 📬 Contact & Community

Join our music archiving community on Discord for support, discussions, and more cool projects:
[![Discord Server](https://img.shields.io/discord/1385439874059866113?color=7289DA&label=Join%20our%20Discord&logo=discord&logoColor=white)]([https://discord.gg/vhPkkXkPGP](https://discord.gg/vhPkkXkPGP))

🎵 **Primarily focused on music preservation and archival**  
🤝 **Get help with this project and others**  
