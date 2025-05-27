from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("🔄 Handling new file request...")
        user = update.effective_user
        name = f"{user.first_name}_{user.last_name or ''}".strip().replace(" ", "_")
        user_id = user.id
        print(f"👤 User: {name} (ID: {user_id})")

        # Create folder with debug
        folder = f"uploads/{name}_{user_id}"
        print(f"📂 Creating folder: {folder}")
        os.makedirs(folder, exist_ok=True, mode=0o777)
        
        # File detection
        if update.message.document:
            file = update.message.document
            file_name = file.file_name
            print(f"📄 Document detected: {file_name}")
        elif update.message.photo:
            file = update.message.photo[-1]
            file_name = f"photo_{update.message.message_id}.jpg"
            print(f"📸 Photo detected, saving as: {file_name}")
        else:
            print("⚠️ Unsupported file type")
            await update.message.reply_text("⚠️ Unsupported file type")
            return

        # Download file
        print("⬇️ Starting download...")
        file_obj = await context.bot.get_file(file.file_id)
        save_path = os.path.abspath(os.path.join(folder, file_name))
        print(f"💾 Save path: {save_path}")
        
        await file_obj.download_to_drive(save_path)
        print("✅ File saved locally")
        
        # Admin forwarding
        try:
            admin_id = int(os.getenv("ADMIN_CHAT_ID", "0"))  # Default to 0 if not set
            if admin_id == 0:
                raise ValueError("ADMIN_CHAT_ID not set")
                
            print(f"📤 Forwarding to admin: {admin_id}")
            with open(save_path, 'rb') as f:
                await context.bot.send_document(
                    chat_id=admin_id,
                    document=f,
                    caption=f"New upload from {name}",
                    filename=f"{name}_{file_name}"
                )
            print("📨 Forwarding complete")
        except Exception as admin_error:
            print(f"❌ Admin forward failed: {str(admin_error)}")

        await update.message.reply_text(f"✅ File '{file_name}' processed successfully!")
        
    except Exception as e:
        error_msg = f"❌ Critical error: {str(e)}"
        print(error_msg)
        await update.message.reply_text("⚠️ An error occurred while processing your file")


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
