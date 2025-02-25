import gdown
import os
import requests
import zipfile

# Google Drive folder ID (replace with your actual folder ID)
folder_id = "your_folder_id_here"

# Destination folder for unzipped files
unzipped_folder = "unzipped_files"

# Ensure the unzipped folder exists
os.makedirs(unzipped_folder, exist_ok=True)

# Get file metadata (list of files in the folder)
metadata_url = f"https://www.googleapis.com/drive/v3/files?q='{folder_id}'+in+parents&fields=files(id,name)"
headers = {"Accept": "application/json"}

response = requests.get(metadata_url, headers=headers)

if response.status_code == 200:
    files = response.json().get("files", [])
    for file in files:
        file_id = file["id"]
        file_name = file["name"]

        # Process only ZIP files
        if file_name.endswith(".zip"):
            # Check if ZIP file already exists
            if os.path.exists(file_name):
                print(f"Skipping {file_name}, already exists.")
            else:
                print(f"Downloading {file_name}...")
                url = f"https://drive.google.com/uc?id={file_id}"
                gdown.download(url, file_name, quiet=False)
                print(f"Downloaded {file_name}")

            # Unzip the file if not already extracted
            extract_path = os.path.join(unzipped_folder, file_name.replace(".zip", ""))
            if not os.path.exists(extract_path):
                print(f"Unzipping {file_name}...")
                with zipfile.ZipFile(file_name, "r") as zip_ref:
                    zip_ref.extractall(extract_path)
                print(f"Extracted to {extract_path}")
            else:
                print(f"Skipping unzip, {file_name} already extracted.")

else:
    print("Failed to retrieve file list. Ensure the folder is public or use authentication.")
