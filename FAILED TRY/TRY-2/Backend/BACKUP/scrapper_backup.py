import requests

# GitHub repository details
repo_owner = 'mithindev'
repo_name = 'mithindev'

# GitHub API endpoint to get repository contents
api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents'

# Make a GET request to the API endpoint
response = requests.get(api_url)

if response.status_code == 200:
    contents = response.json()

    # Loop through each item in the contents
    for item in contents:
        if item['type'] == 'file':
            file_url = item['download_url']
            file_name = item['name']

            # Make a GET request to download the file content
            file_response = requests.get(file_url)

            if file_response.status_code == 200:
                file_content = file_response.content.decode('utf-8')

                # Append the content to a text file with UTF-8 encoding
                with open(f'{repo_name}_contents.txt', 'a', encoding='utf-8') as f:
                    f.write(f'File: {file_name}\n')
                    f.write(file_content)
                    f.write('\n\n')
            else:
                print(f'Failed to download {file_name}')

    print('Repository content scraped and saved.')
else:
    print('Failed to fetch repository contents.')
