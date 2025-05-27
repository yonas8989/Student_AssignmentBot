import os
import shutil
from datetime import datetime
from telegram import Bot
from configparser import ConfigParser

config = ConfigParser()
config.read('backup_config.ini')

def download_files():
    bot = Bot(token=config['Telegram']['bot_token'])
    updates = bot.get_updates(offset=config.getint('Settings','last_offset', fallback=0))
    
    new_offset = updates[-1].update_id + 1 if updates else 0
    backup_dir = os.path.join('..','archives', datetime.now().strftime("%Y%m%d"))
    
    os.makedirs(backup_dir, exist_ok=True)
    
    for update in updates:
        if update.message and update.message.document:
            file = update.message.document
            file.download(custom_path=os.path.join(backup_dir, file.file_name))
    
    # Update config
    config['Settings']['last_offset'] = str(new_offset)
    with open('backup_config.ini', 'w') as f:
        config.write(f)

def create_zip():
    today = datetime.now().strftime("%Y%m%d")
    shutil.make_archive(
        os.path.join('..','archives', f'backup_{today}'),
        'zip',
        os.path.join('..','archives', today)
    )

if __name__ == "__main__":
    download_files()
    create_zip()
    print("✅ Backup completed")