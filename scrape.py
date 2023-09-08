import requests
import os
from decouple import config
from urllib.parse import urlparse

def fetch_files_and_save_content(github_repo_url, github_token, output_file, exclude_extensions=None):
    parsed_url = urlparse(github_repo_url)
    if parsed_url.netloc != 'github.com':
        raise ValueError("Invalid GitHub repository URL")

    github_username, github_repo_name = parsed_url.path.strip('/').split('/')
    base_url = f'https://api.github.com/repos/{github_username}/{github_repo_name}/contents/'
    headers = {'Authorization': f'token {github_token}'}

    if exclude_extensions is None:
        exclude_extensions = []

    response = requests.get(base_url, headers=headers)
    data = response.json()

    for item in data:
        if item['type'] == 'file':
            file_name = item['name']
            file_extension = os.path.splitext(file_name)[1].lower()  # Get the file extension in lowercase
            if file_extension not in exclude_extensions:
                print(f"Downloading file: {item['path']}")
                file_url = item['download_url']
                file_content = requests.get(file_url).text
                with open(output_file, 'a', encoding='utf-8') as file:
                    file.write(f"File: {item['path']}\n")
                    file.write(file_content)
                    file.write('\n\n')
        elif item['type'] == 'dir':
            fetch_files_and_save_content(github_repo_url, github_token, output_file, exclude_extensions)
