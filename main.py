import os
import logging
from datetime import date
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from services.stt import transcribe_audio
from services.llm import analyze_and_respond
from services.tts import text_to_speech

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_TELEGRAM_ID = int(os.getenv("ADMIN_TELEGRAM_ID", "0"))
DAILY_USAGE_LIMIT = int(os.getenv("DAILY_USAGE_LIMIT", "5"))

user_usage_tracker = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def check_and_update_limit(user_id: int) -> tuple[bool, int]:
    if user_id == ADMIN_TELEGRAM_ID:
        return True, 999

    today = str(date.today())
    
    if today not in user_usage_tracker:
        user_usage_tracker.clear() 
        user_usage_tracker[today] = {}

    current_usage = user_usage_tracker[today].get(user_id, 0)

    if current_usage >= DAILY_USAGE_LIMIT:
        return False, 0

    user_usage_tracker[today][user_id] = current_usage + 1
    remaining = DAILY_USAGE_LIMIT - (current_usage + 1)
    return True, remaining

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Hello! I'm Maryana, your English practice assistant.\n\n"
        "Send me a voice note in English, and I will:\n"
        "1. Check your grammar and vocabulary\n"
        "2. Provide feedback\n"
        "3. Reply with a follow-up question to keep chatting!"
    )
    await update.message.reply_text(welcome_text)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text("Listening and analyzing your voice note...")
    
    ogg_path = None
    tts_audio_path = None

    try:
        voice_file = await context.bot.get_file(update.message.voice.file_id)
        ogg_path = f"user_voice_{update.message.message_id}.ogg"
        await voice_file.download_to_drive(ogg_path)

        user_text = transcribe_audio(ogg_path)
        
        if not user_text:
            await status_msg.edit_text("Sorry, I couldn't hear any clear audio. Please try again!")
            return

        analysis = analyze_and_respond(user_text)

        feedback_text = f" **What I heard:**\n\"{user_text}\"\n\n"
        
        if analysis.get("has_errors") and analysis.get("corrections"):
            feedback_text += " ** Feedback & Corrections:**\n"
            for corr in analysis["corrections"]:
                feedback_text += f"• ~ {corr['original']}~ ~**{corr['suggestion']}**\n  _{corr['explanation']}_\n"
            feedback_text += f"\n ** Better way to say it:**\n\"{analysis['improved_sentence']}\"\n\n"
        else:
            feedback_text += " ** Great job!** No major grammar issues found.\n\n"

        feedback_text += f" ** Next Question:**\n{analysis['next_question']}"

        tts_audio_path = f"bot_reply_{update.message.message_id}.mp3"
        await text_to_speech(analysis['next_question'], tts_audio_path)

        await status_msg.edit_text(feedback_text, parse_mode="Markdown")
        
        if tts_audio_path and os.path.exists(tts_audio_path) and os.path.getsize(tts_audio_path) > 0:
            with open(tts_audio_path, 'rb') as audio:
                await update.message.reply_voice(voice=audio)

    except Exception as e:
        print(f"Error on handle_voice: {e}")
        await status_msg.edit_text("An error occurred while processing your voice note.")

    finally:
        if ogg_path and os.path.exists(ogg_path):
            os.remove(ogg_path)
        if tts_audio_path and os.path.exists(tts_audio_path):
            os.remove(tts_audio_path)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("Telegram Bot")
    app.run_polling()

if __name__ == "__main__":
    main()