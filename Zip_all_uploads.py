import os
import shutil
from datetime import datetime

def zip_student_uploads():
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        print("No uploads found.")
        return

    zip_name = f"full_assignment_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    zip_path = os.path.join("backups", zip_name)

    os.makedirs("backups", exist_ok=True)
    shutil.make_archive(zip_path.replace(".zip", ""), 'zip', uploads_dir)

    print(f"✅ All uploads zipped into: {zip_path}")

if __name__ == "__main__":
    zip_student_uploads()
