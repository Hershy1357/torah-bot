# How to run on Replit — Step by Step

## PART A — Get File IDs (do this first)

### 1. Go to replit.com
- Sign up free (use Google account)

### 2. Create a new Repl
- Click **+ Create Repl**
- Choose **Python**
- Name it: `helper-bot`
- Click **Create Repl**

### 3. Upload files
Click the files icon on the left, then upload:
- `helper_bot.py`
- `data.py`

### 4. Add your token
- Click on `helper_bot.py`
- Find this line:
  ```
  BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
  ```
- Change to your token:
  ```
  BOT_TOKEN = os.environ.get("BOT_TOKEN", "8527698073:AAH3ON38Qss8lsZQLso2HVkjneH_l6M2HFI")
  ```

### 5. Change main file
- Click the 3 dots next to `helper_bot.py`
- Click **Set as main file**

### 6. Click the big green RUN button ▶
- You'll see: `Helper bot running – forward files to get their file_id`

### 7. Go to Telegram
- Open **@chumashrashibot**
- Forward audio files from your channel one by one
- The bot replies with a code like: `BQACAgIAAxkBAAIBnmX...`
- Copy each code into `data.py` replacing the matching `"TODO"`

---

## PART B — Run the real bot

### 1. Create another Repl
- Click **+ Create Repl**
- Choose **Python**
- Name it: `torah-bot`

### 2. Upload files
Upload all 4 files:
- `bot.py`
- `data.py` (the filled one with all file_ids!)
- `helper_bot.py`
- `pyproject.toml`

### 3. Add your token safely
- Click **Secrets** (🔒 lock icon on the left sidebar)
- Click **+ New Secret**
- Key: `BOT_TOKEN`
- Value: `8527698073:AAH3ON38Qss8lsZQLso2HVkjneH_l6M2HFI`

### 4. Click RUN ▶
Your bot is live! 🎉

---

## Keep the bot running 24/7 (free)
Replit stops after 1 hour of no activity.
To keep it always on:
- Go to **UptimeRobot.com** (free)
- Sign up and add your Replit URL as a monitor
- It pings your bot every 5 minutes — keeps it alive!

---

## Summary of files
| File | What it does |
|------|-------------|
| `bot.py` | The main Torah bot |
| `data.py` | All file_ids for audio + PDF |
| `helper_bot.py` | Tool to get file_ids (run once) |
| `pyproject.toml` | Tells Replit what to install |
