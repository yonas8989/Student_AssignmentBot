from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = f"{user.first_name}_{user.last_name or ''}".strip().replace(" ", "_")
    folder = f"uploads/{name}"
    os.makedirs(folder, exist_ok=True)

    file = update.message.document or update.message.photo[-1]
    file_obj = await context.bot.get_file(file.file_id)
    file_name = getattr(file, 'file_name', 'photo.jpg')
    save_path = os.path.join(folder, file_name)

    await file_obj.download_to_drive(save_path)
    await update.message.reply_text(f"✅ File saved for {name}!")
    print(f"Received file from: {name}")
    print(f"Saving to: {save_path}")



def main():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in .env file")

    app = ApplicationBuilder().token(bot_token).build()
    file_handler = MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file)
    app.add_handler(file_handler)
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
