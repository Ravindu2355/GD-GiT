import os
import requests

def download_from_drive(folder_id):
    os.makedirs('downloads', exist_ok=True)
    dummy_file = 'downloads/sample.mp4'
    with open(dummy_file, 'wb') as f:
        f.write(os.urandom(5 * 1024 * 1024))
    return [{
        'name': 'sample.mp4',
        'size': os.path.getsize(dummy_file),
        'path': dummy_file
    }]