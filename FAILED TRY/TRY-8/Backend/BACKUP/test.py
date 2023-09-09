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
        if item.get('type') == 'file':  # Use .get() to safely access the 'type' key
            print(f"File: {item['name']}")  # Use 'name' to get the file or folder name
        elif item.get('type') == 'dir':
            print(f"Folder: {item['name']}")  # Use 'name' to get the file or folder name
            fetch_files_and_folders(item['url'])

# Start scraping from the root directory
fetch_files_and_folders(base_url)
