import requests
import os

# Replace 'YOUR_PERSONAL_ACCESS_TOKEN' with your actual PAT
PERSONAL_ACCESS_TOKEN = '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'

# Define your User-Agent
user_agent = 'CodeEngage'

def scrape_github_repository(repo_url, output_dir=''):
    # Extract owner and repository name from the URL
    url_parts = repo_url.split('/')
    repo_owner = url_parts[-2]
    repo_name = url_parts[-1]

    # GitHub API endpoint to get repository contents
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents'

    # Make a GET request to the API endpoint with authentication
    headers = {
        'Authorization': f'token {PERSONAL_ACCESS_TOKEN}',
        'User-Agent': user_agent
    }
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        contents = response.json()

        # Create the output directory if it doesn't exist
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Loop through each item in the contents
        for item in contents:
            if item['type'] == 'file':
                file_url = item.get('download_url')  # Use .get() to handle None
                if file_url is not None:
                    file_name = item['name']

                    # Make a GET request to download the file content
                    file_response = requests.get(file_url, headers=headers)

                    if file_response.status_code == 200:
                        file_content = file_response.content.decode('utf-8')

                        # Determine the file path in the output directory
                        file_path = os.path.join(output_dir, file_name)

                        # Write the content to the file with UTF-8 encoding
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(file_content)
                    else:
                        print(f'Failed to download {file_name}')
                else:
                    print(f'Skipping item with no download_url')
            elif item['type'] == 'dir':
                # Recursively scrape the contents of subfolders
                subdir_url = item['url']
                subdir_name = item['name']
                subdir_output_dir = os.path.join(output_dir, subdir_name)
                scrape_github_repository(subdir_url, subdir_output_dir)

        print('Repository content scraped and saved.')
    else:
        print('Failed to fetch repository contents.')

# Example usage
repository_url = 'https://github.com/mithindev/COLLEGE'
scrape_github_repository(repository_url, output_dir='output_folder')
