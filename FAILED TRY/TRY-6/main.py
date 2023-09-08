from scrapper import scrape_github_repo
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


# Now you can use the github_token variable in your code

if __name__ == "__main__":
    # Replace these variables with your GitHub repo URL, GitHub token, and output file
    repo_url = 'https://github.com/mithindev/FoundIt'
    output_file = 'contents.txt'

    github_token = os.getenv("GITHUB_TOKEN")


    scrape_github_repo(repo_url, github_token, output_file)