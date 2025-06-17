from github import Github
import os

def upload_file(filepath, github):
    g = Github(github['token'])
    repo = g.get_user(github['username']).get_repo(github['repo'])
    with open(filepath, 'rb') as f:
        content = f.read()
    repo_path = os.path.join(github['folder'], os.path.basename(filepath))
    repo.create_file(repo_path, f"Upload {os.path.basename(filepath)}", content, branch="main")

def upload_folder(folder_path, github):
    for root, _, files in os.walk(folder_path):
        for file in files:
            full = os.path.join(root, file)
            relative = os.path.relpath(full, folder_path)
            with open(full, 'rb') as f:
                content = f.read()
            g = Github(github['token'])
            repo = g.get_user(github['username']).get_repo(github['repo'])
            path = os.path.join(github['folder'], os.path.basename(folder_path), relative)
            repo.create_file(path, f"Upload {file}", content, branch="main")