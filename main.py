from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("🔄 Handling new file...")
        user = update.effective_user
        name = f"{user.first_name}_{user.last_name or ''}".strip().replace(" ", "_")
        user_id = user.id

        # Create user folder
        folder = f"uploads/{name}_{user_id}"
        os.makedirs(folder, exist_ok=True)

        # Detect file type and prepare for forwarding
        file_to_forward = None
        file_name = ""
        
        if update.message.document:
            file = update.message.document
            file_name = file.file_name
            file_to_forward = file
        elif update.message.photo:
            file = update.message.photo[-1]
            file_name = f"photo_{update.message.message_id}.jpg"
            file_to_forward = file  # We'll handle photos differently when forwarding

        # Download file
        file_obj = await context.bot.get_file(file.file_id)
        save_path = os.path.join(folder, file_name)
        await file_obj.download_to_drive(save_path)

        # Forward to admin
        admin_id = int(os.getenv("ADMIN_CHAT_ID"))
        if admin_id:
            try:
                if update.message.document:
                    await context.bot.send_document(
                        chat_id=admin_id,
                        document=file_to_forward.file_id,
                        caption=f"New document from {name} (ID: {user_id})"
                    )
                elif update.message.photo:
                    await context.bot.send_photo(
                        chat_id=admin_id,
                        photo=file_to_forward.file_id,
                        caption=f"New photo from {name} (ID: {user_id})"
                    )
                print(f"📨 Forwarded to admin: {admin_id}")
            except Exception as e:
                print(f"❌ Admin forward failed: {e}")

        await update.message.reply_text(f"✅ File saved: {file_name}")

    except Exception as e:
        print(f"❌ Error: {e}")
        await update.message.reply_text("⚠️ Processing failed")

async def zip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin-only /zip command"""
    admin_id = int(os.getenv("ADMIN_CHAT_ID"))
    if update.effective_user.id != admin_id:
        await update.message.reply_text("❌ Admin only!")
        return

    await update.message.reply_text("⏳ Creating ZIP...")
    from Zip_all_uploads import zip_student_uploads
    zip_path = zip_student_uploads()

    if zip_path:
        with open(zip_path, 'rb') as f:
            await update.message.reply_document(f, caption="📦 All uploads")
        os.remove(zip_path)  # Cleanup
    else:
        await update.message.reply_text("⚠️ No files found")

def main():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file))
    app.add_handler(CommandHandler("zip", zip_command))
    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()