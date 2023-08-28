import requests

owner = "mithindev"
repository = "CodeEngage"

# Construct the API URL to list contents of the repository
api_url = f"https://api.github.com/repos/{owner}/{repository}/contents"

# Make a GET request to the GitHub API
response = requests.get(api_url)

if response.status_code == 200:
    # Parse the JSON response
    repo_contents = response.json()

    for content in repo_contents:
        if content.get('type') == 'file':
            file_url = content['download_url']
            file_name = content['name']

            # Make a GET request to download the file
            file_response = requests.get(file_url)

            if file_response.status_code == 200:
                # Display the file content
                file_content = file_response.text
                print(f"Content of {file_name}:")
                print(file_content)
                print("=" * 50)  # Separation line
            else:
                print(f"Error downloading {file_name}: {file_response.status_code}")
else:
    print(f"Error listing contents: {response.status_code}")
