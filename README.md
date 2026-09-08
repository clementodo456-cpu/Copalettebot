# Img2basebot (@Img2basebot)

Img2basebot is a production-ready Telegram Bot built with Python 3.11+ and aiogram 3.x. It converts uploaded images into Base64 encoded strings and Data URIs for use in web design, web APIs, and database storage.

## Features
- **Multiple Upload Options:** Accepts native Telegram photo uploads and full-resolution uncompressed image documents.
- **Supported Formats:** JPG/JPEG, PNG, WEBP, and GIF.
- **Dual Output Formats:** Provides raw Base64 string or ready-to-use Data URI (`data:image/...;base64,...`).
- **Large Result Handling:** Delivers inline text for standard payloads, automatically generating `.txt` file attachments if string lengths exceed Telegram's 4,000 character limit.
- **Metadata Reporting:** Displays dimension resolution, MIME types, format types, original size, and encoded size.
- **Resource Management:** Automatic deletion of temporary files and sandboxed per-user state tracking.

---

## Local Setup

### Prerequisites
- Python 3.11 or higher installed locally.
- Git installed.

### 1. Bot Registration via BotFather
1. Message `@BotFather` on Telegram.
2. Issue `/newbot` command and specify bot name and username (e.g., `Img2basebot`).
3. Save the HTTP API BOT_TOKEN provided by BotFather.

### 2. Repository Configuration
```bash
git clone [https://github.com/your-username/img2basebot.git](https://github.com/your-username/img2basebot.git)
cd img2basebot

python -m venv venv
source venv/bin/venv/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
