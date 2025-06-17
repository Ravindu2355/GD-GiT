import time
import os
import ffmpeg
from gdrive_downloader import download_from_drive
from github_uploader import upload_file, upload_folder

def convert_to_hls(input_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'index.m3u8')
    ffmpeg.input(input_path).output(
        output_path,
        format='hls',
        hls_time=10,
        hls_segment_filename=os.path.join(output_dir, 'segment_%03d.ts')
    ).run()

def run(config, session, save_session, lock):
    drive_id = config['drive_id']
    format_under_25mb = config['format']
    github = {
        'token': config['gh_token'],
        'username': config['gh_user'],
        'repo': config['gh_repo'],
        'folder': config.get('gh_dir', '')
    }

    files = download_from_drive(drive_id)
    for file in files:
        if session.get('paused'):
            while session.get('paused'):
                time.sleep(2)
        name, size, path = file['name'], file['size'], file['path']
        with lock:
            session['progress'][name] = {'status': 'processing', 'eta': '...'}
            save_session(session)

        if size < 25 * 1024 * 1024:
            ext = '.' + format_under_25mb
            new_path = os.path.splitext(path)[0] + ext
            os.rename(path, new_path)
            upload_file(new_path, github)
        else:
            output_dir = os.path.splitext(path)[0] + '_hls'
            convert_to_hls(path, output_dir)
            upload_folder(output_dir, github)

        with lock:
            session['progress'][name] = {'status': 'done'}
            save_session(session)