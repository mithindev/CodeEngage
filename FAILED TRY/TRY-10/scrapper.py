import os
from github import Github

class GithubRepoScraper:
    """Scrape GitHub repositories."""
    def __init__(self, repo_name, github_token=None):
        self.github_token = github_token
        self.repo_name = repo_name
        self.exclude_extensions = {".ppt", ".pptx", ".mp3", ".wav", ".mp4", ".avi", ".png", ".jpg", ".jpeg", ".gif", ".bmp"}

    def should_exclude_file(self, file_name):
        """Check if a file should be excluded based on its extension."""
        _, file_extension = os.path.splitext(file_name.lower())
        return file_extension in self.exclude_extensions

    def fetch_all_files(self):
        """Fetch all files from the GitHub repository, excluding specified extensions."""
        github_instance = Github(self.github_token)
        repo = github_instance.get_repo(self.repo_name)
        contents = repo.get_contents("")
        files_data = []

        def recursive_fetch_files(contents):
            for content_file in contents:
                if content_file.type == "dir":
                    recursive_fetch_files(repo.get_contents(content_file.path))
                else:
                    file_name = content_file.name
                    if not self.should_exclude_file(file_name):
                        file_content = content_file.decoded_content.decode("utf-8")
                        files_data.append((file_name, file_content))

        recursive_fetch_files(contents)
        return files_data

    def write_to_file(self, files_data, output_file):
        """Write the repository files to a text file."""
        with open(output_file, "w", encoding='utf-8') as f:
            for file_name, content in files_data:
                f.write(f"File: {file_name}\n")
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
