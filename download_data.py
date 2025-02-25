import gdown
import zipfile
import os
import shutil

# Google Drive file ID (replace with your actual file ID)
file_id = "1qBRWbMQdiLk6g8vi7Rbga3DJ8Gb4qL1G"

# Destination file paths
zip_file = "downloaded_file.zip"
extracted_folder = "extracted_content"
data_folder = "data"
os.makedirs(data_folder, exist_ok=True)

# Download the ZIP file
gdown.download(f"https://drive.google.com/uc?id={file_id}", zip_file, quiet=False)

# Extract the ZIP file
with zipfile.ZipFile(zip_file, "r") as zip_ref:
    zip_ref.extractall(extracted_folder)

# Move the contents of extracted subfolders to 'data' directory
for root, dirs, files in os.walk(extracted_folder):
    for name in dirs:
        source_dir = os.path.join(root, name)
        shutil.move(source_dir, data_folder)

# Clean up: delete the downloaded ZIP file and the extracted folder
os.remove(zip_file)
shutil.rmtree(extracted_folder)

print(f"All subfolder contents moved to '{data_folder}' and cleanup completed.")

