from decouple import config
from scrape import fetch_files_and_save_content

# Get the GitHub repository URL and token as user input
github_repo_url = input("Enter the GitHub repository URL: ")
token = config('GITHUB_TOKEN')

# Specify the output file where content will be saved
output_file = 'github_repo_content.txt'

# Call the fetch_files_and_save_content function with user-provided input
fetch_files_and_save_content(github_repo_url, token, output_file)

print(f"Content from the GitHub repository has been saved to {output_file}")
