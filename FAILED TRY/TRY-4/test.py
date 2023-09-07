import requests
import os

# Replace these variables with your GitHub username, repository name, and Personal Access Token
username = 'mithindev'
repo_name = 'Leet-Code-Questions'
token = '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'

# Define the GitHub API endpoint
base_url = f'https://api.github.com/repos/{username}/{repo_name}/contents/'

# Function to fetch files and folders recursively
def fetch_files_and_folders(url):
    try:
        response = requests.get(url, headers={'Authorization': f'token {token}'})
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        if isinstance(data, list):
            for item in data:
                if item.get('type') == 'file':
                    print(f"File: {item['path']}")
                elif item.get('type') == 'dir':
                    print(f"Folder: {item['path']}")
                    fetch_files_and_folders(item['url'])
        else:
            print(f"Unexpected response data: {data}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Start scraping from the root directory
fetch_files_and_folders(base_url)
