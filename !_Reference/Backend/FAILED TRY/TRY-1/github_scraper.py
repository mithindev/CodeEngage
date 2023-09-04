import requests
from bs4 import BeautifulSoup

# Define the target repository and file path
repo_owner = "mithindev"
repo_name = "CodeEngage"

# Send a GET request to the repository file page
url = f"https://github.com/{repo_owner}/{repo_name}"
response = requests.get(url)

# Parse the HTML content of the response
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the code blocks in the file content
code_blocks = soup.find_all('div', class_='highlight')

# Extract all code from code blocks
code = ""
for code_block in code_blocks:
    code += code_block.text

# Write code to file
with open("output.txt", "w") as f:
    f.write(code)


print("Done!")
