import os
import re
import requests
from bs4 import BeautifulSoup

def get_files_from_public_folder(folder_id, allowed_exts=None):
    if allowed_exts is None:
        allowed_exts = ['.mp4', '.txt', '.mkv', '.srt', '.ass']

    url = f"https://drive.google.com/drive/folders/{folder_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    file_regex = re.compile(r'"(https://drive.google.com/file/d/([^/]+))/view\?usp=drive_link"')
    files = []

    for match in file_regex.finditer(response.text):
        full_url, file_id = match.groups()
        name_match = re.search(r'aria-label="([^"]+)"', response.text[match.start():match.end()])
        filename = name_match.group(1) if name_match else f"{file_id}.bin"
        ext = os.path.splitext(filename)[-1].lower()
        if ext in allowed_exts:
            files.append({
                "id": file_id,
                "name": filename
            })

    return files

def download_file(file_id, filename):
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    os.makedirs("downloads", exist_ok=True)
    path = os.path.join("downloads", filename)

    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return {
        "name": filename,
        "size": os.path.getsize(path),
        "path": path
    }

def download_from_drive(folder_id):
    files = get_files_from_public_folder(folder_id)
    results = []
    for file in files:
        print(f"Downloading {file['name']}...")
        info = download_file(file['id'], file['name'])
        results.append(info)
    return results
