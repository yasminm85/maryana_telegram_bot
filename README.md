
# Maryana English Tutor Bot

Maryana is a bot that can help you improve your English skills especially speaking by correcting your grammar, asking questions, and providing voice note analysis.


## Demo

[maryana-bot](https://t.me/maryana_tutor_bot)
## Features

- Voice-to-Text Transcript
- Grammar Feedback
- Text-to-Speech


## Tech Stack

**Language:** Python 3.9+

**Speech-to-Text:** Groq API

**Bot Framework:** python-telegram-bot

**LLM Engine:** Deepseek API

**Text-to-Speech:** edge-tts



## Installation

Ensure your system has installed:
- Python 3.9+
- FFmpeg
```bash
  brew install ffmpeg
```
    
## Clone Repository & Environment Variables

To run this project, you will need to add the following environment variables to your .env file

git clone [github repository](https://github.com/yasminm85/maryana_telegram_bot.git)

```bash
cd maryana_telegram_bot

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

```bash
TELEGRAM_BOT_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
ADMIN_TELEGRAM_ID=123456789
DAILY_USAGE_LIMIT=
```


## Authors

- [@yasmine](https://www.github.com/yasminm85)

