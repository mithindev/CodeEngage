import os
from github import Github

class GithubRepoScraper:
    """Scrape GitHub repositories."""
    def __init__(self, repo_name, github_token=None):
        self.github_token = github_token
        self.repo_name = repo_name

    def fetch_all_files(self):
        """Fetch all files from the GitHub repository."""
        github_instance = Github(self.github_token)
        repo = github_instance.get_repo(self.repo_name)
        contents = repo.get_contents("")
        files_data = []

        def recursive_fetch_files(contents):
            for content_file in contents:
                if content_file.type == "dir":
                    recursive_fetch_files(repo.get_contents(content_file.path))
                else:
                    file_content = content_file.decoded_content.decode("utf-8")
                    files_data.append((content_file.path, file_content))

        recursive_fetch_files(contents)
        return files_data

    def write_to_file(self, files_data, output_file):
        """Write the repository files to a text file."""
        with open(output_file, "w", encoding='utf-8') as f:
            for path, content in files_data:
                f.write(f"File: {path}\n")
                f.write(content)
                f.write('\n' + '-' * 50 + '\n')

    def scrape_repository(self, output_file):
        """Scrape the entire GitHub repository and save it to a text file."""
        files_data = self.fetch_all_files()
        self.write_to_file(files_data, output_file)

# Example usage:
repo_name = "mithindev/mithindev"  # Replace with the GitHub repository name (owner/repo)
github_token = "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"  # Replace with your GitHub Personal Access Token
output_file = "data/repository_contents.txt"  # Replace with the desired output file name

scraper = GithubRepoScraper(repo_name, github_token)
scraper.scrape_repository(output_file)
