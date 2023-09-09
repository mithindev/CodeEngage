import requests
import os

# Replace these variables with your GitHub username, repository name, and Personal Access Token
username = 'mithindev'
repo_name = 'COLLEGE'
token = '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'

# Define the GitHub API endpoint
base_url = f'https://api.github.com/repos/{username}/{repo_name}/contents/'

# Function to fetch files and folders recursively
def fetch_files_and_folders(url):
    response = requests.get(url, headers={'Authorization': f'token {token}'})
    data = response.json()
    
    for item in data:
        if item['type'] == 'file':
            print(f"File: {item['path']}")
        elif item['type'] == 'dir':
            print(f"Folder: {item['path']}")
            fetch_files_and_folders(item['url'])

# Start scraping from the root directory
fetch_files_and_folders(base_url)

