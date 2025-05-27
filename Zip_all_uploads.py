import os
import shutil
from datetime import datetime

def zip_student_uploads():
    """Zips all uploads and returns the path to the zip file"""
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir) or not os.listdir(uploads_dir):
        print("No uploads found.")
        return None

    # Create backups directory if it doesn't exist
    os.makedirs("backups", exist_ok=True)
    
    # Generate timestamped zip name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_name = f"student_uploads_{timestamp}.zip"
    zip_path = os.path.join("backups", zip_name)

    # Create the zip archive
    shutil.make_archive(zip_path.replace(".zip", ""), 'zip', uploads_dir)
    
    print(f"✅ All uploads zipped into: {zip_path}")
    return zip_path

if __name__ == "__main__":
    zip_student_uploads()