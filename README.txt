# 📚 Student Assignment Bot

A Telegram bot that collects student submissions, forwards them to admins, and provides zip archive functionality.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https%3A%2F%2Fgithub.com%2Fyourusername%2FStudentAssignmentBot)

## ✨ Features

- **File Collection**: Accepts documents and photos from students
- **Admin Forwarding**: Instant file forwarding to admin
- **Zip Archives**: Generate complete backups with `/zip` command
- **Organized Storage**: Files stored in `uploads/{student_name_id}/`
- **Automatic Backups**: Zips saved in `backups/` with timestamps

## 🛠 Setup

### Prerequisites
- Python 3.8+
- Telegram bot token from [@BotFather](https://t.me/BotFather)
- Railway account (for deployment)

### Local Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/yonas8989/StudentAssignmentBot.git
   cd StudentAssignmentBot