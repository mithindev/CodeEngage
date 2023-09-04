import requests
import os

# Replace these variables with your GitHub username, repository name, and Personal Access Token
username = 'mithindev'
repo_name = 'NoteSnip'
token = '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'

# Define the GitHub API endpoint
base_url = f'https://api.github.com/repos/{username}/{repo_name}/contents/'

# Function to fetch files and folders recursively and save content
def fetch_files_and_save_content(url, output_file):
    response = requests.get(url, headers={'Authorization': f'token {token}'})
    data = response.json()
    
    for item in data:
        if item['type'] == 'file':
            print(f"Downloading file: {item['path']}")
            file_url = item['download_url']
            file_content = requests.get(file_url).text
            with open(output_file, 'a', encoding='utf-8') as file:
                file.write(f"File: {item['path']}\n")
                file.write(file_content)
                file.write('\n\n')
        elif item['type'] == 'dir':
            fetch_files_and_save_content(item['url'], output_file)

# Specify the output file where content will be saved
output_file = 'github_repo_content.txt'

# Start scraping from the root directory
fetch_files_and_save_content(base_url, output_file)
