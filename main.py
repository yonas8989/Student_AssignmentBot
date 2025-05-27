from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Get user information
        user = update.effective_user
        name = f"{user.first_name}_{user.last_name or ''}".strip().replace(" ", "_")
        user_id = user.id
        
        # Create user-specific folder
        folder = f"uploads/{name}_{user_id}"
        os.makedirs(folder, exist_ok=True)

        # Determine if it's a document or photo
        if update.message.document:
            file = update.message.document
            file_name = file.file_name
        elif update.message.photo:
            file = update.message.photo[-1]  # Get highest resolution photo
            file_name = f"photo_{update.message.message_id}.jpg"
        else:
            await update.message.reply_text("⚠️ Unsupported file type")
            return

        # Download the file
        file_obj = await context.bot.get_file(file.file_id)
        save_path = os.path.join(folder, file_name)
        await file_obj.download_to_drive(save_path)
        
        # Send confirmation to user
        await update.message.reply_text(
            f"✅ File received from {user.first_name}!\n"
            f"📄 Filename: {file_name}\n"
            f"💾 Saved to our system."
        )
        
        # Send copy to admin (you)
        admin_id = int(os.getenv("ADMIN_CHAT_ID"))  # Your Telegram ID in Railway variables
        try:
            await context.bot.send_document(
                chat_id=admin_id,
                document=open(save_path, 'rb'),
                caption=(
                    f"📤 New upload\n"
                    f"👤 From: {user.first_name} {user.last_name or ''}\n"
                    f"🆔 User ID: {user_id}\n"
                    f"📂 Filename: {file_name}"
                ),
                filename=f"{name}_{file_name}"
            )
        except Exception as admin_error:
            print(f"Failed to send to admin: {admin_error}")
            
        # Log the upload
        print(f"📥 Received {file_name} from {name} (ID: {user_id})")
        print(f"💾 Saved to: {save_path}")
        
    except Exception as e:
        print(f"❌ Error handling file: {e}")
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
