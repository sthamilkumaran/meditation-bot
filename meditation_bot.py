import os
import random

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

# Load BOT_TOKEN from .env file
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

meditations = {
    "Relaxation": [
        "Close your eyes and take 5 slow, deep breaths…",
        "Focus on the feeling of your body sinking into your chair.",
        "Release the tension from your shoulders with each exhale."
    ],
    "Focus": [
        "Take a deep breath and count 4 in, 4 hold, 4 out, 4 hold. Repeat.",
        "Bring your attention to your breath. If your mind wanders, gently return.",
        "Notice 3 things you can see, hear, and feel around you."
    ],
    "Sleep": [
        "Lie down, breathe deeply, and imagine a calm, safe place.",
        "Let go of your thoughts and feel the weight of your body on the bed.",
        "Picture each part of your body relaxing, starting from your toes up."
    ]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(theme, callback_data=theme) for theme in meditations.keys()]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🧘 Welcome to Meditation Bot!\n\nChoose a theme to begin:",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🙏 How to use Meditation Bot:\n"
        "- /start → Choose a meditation theme.\n"
        "- Click a theme button → Get a random meditation exercise.\n"
        "- You can come back anytime when you need a mindful break. 🌸"
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    theme = query.data
    exercise = random.choice(meditations[theme])
    await query.edit_message_text(
        f"🌸 *{theme} Meditation:*\n\n{exercise}",
        parse_mode='Markdown'
    )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "😕 Sorry, I didn’t understand that command. Try /start or /help."
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    print("Bot is running…")
    app.run_polling()

if __name__ == "__main__":
    main()
