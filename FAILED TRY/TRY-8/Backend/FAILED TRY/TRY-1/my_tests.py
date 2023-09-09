from github_scraper import scrape_repository_and_save_to_file

repo_url = "https://github.com/mithindev/CodeEngage"
output_file = "repository_files.txt"

scrape_repository_and_save_to_file(repo_url, output_file)
