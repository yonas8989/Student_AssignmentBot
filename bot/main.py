import os
from pathlib import Path
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Initialize environment
load_dotenv()
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True, parents=True)

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # User information
        user = update.effective_user
        user_id = user.id
        clean_name = f"{user.first_name or 'user'}_{user_id}"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # File detection with validation
        if update.message.document:
            file = update.message.document
            file_name = f"{timestamp}_{file.file_name}"
        elif update.message.photo:
            file = update.message.photo[-1]
            file_name = f"{timestamp}_photo.jpg"
        else:
            await update.message.reply_text("⚠️ Only documents and photos are accepted")
            return

        # Size limit (20MB)
        if file.file_size > 20 * 1024 * 1024:
            await update.message.reply_text("⚠️ File exceeds 20MB limit")
            return

        # Save file
        user_dir = UPLOADS_DIR / clean_name
        user_dir.mkdir(exist_ok=True)
        save_path = user_dir / file_name
        
        file_obj = await context.bot.get_file(file.file_id)
        await file_obj.download_to_drive(save_path)

        # Admin notification
        if admin_id := os.getenv("ADMIN_CHAT_ID"):
            try:
                caption = (
                    f"📤 New submission\n"
                    f"👤 {user.first_name} {user.last_name or ''}\n"
                    f"🆔 {user_id}\n"
                    f"📦 {file.file_size//1024}KB\n"
                    f"🕒 {timestamp.replace('_', ' ')}"
                )
                await context.bot.send_document(
                    chat_id=int(admin_id),
                    document=save_path.open('rb'),
                    caption=caption,
                    filename=file_name
                )
            except Exception as e:
                print(f"⚠️ Admin notify failed: {e}")

        await update.message.reply_text(
            f"✅ Received {file_name.split('_')[-1]}\n"
            f"Saved for grading"
        )

    except Exception as e:
        print(f"❌ Error: {e}")
        await update.message.reply_text("⚠️ Processing failed. Please try again.")

def main():
    app = ApplicationBuilder() \
        .token(os.getenv("TELEGRAM_BOT_TOKEN")) \
        .post_init(lambda _: print("🤖 Bot initialized")) \
        .build()
        
    app.add_handler(MessageHandler(
        filters.Document.ALL | filters.PHOTO,
        handle_file
    ))
    
    print("🚀 Starting bot...")
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        close_loop=False
    )

if __name__ == "__main__":
    main()