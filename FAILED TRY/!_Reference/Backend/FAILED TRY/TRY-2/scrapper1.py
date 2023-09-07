import requests
from bs4 import BeautifulSoup
import json

# the URL of the target repo to scrape
url = 'https://github.com/luminati-io/luminati-proxy'

# download the target page
page = requests.get(url)
# parse the HTML document returned by the server
soup = BeautifulSoup(page.text, 'html.parser')

# initialize the object that will contain
# the scraped data
repo = {}

# repo scraping logic
name_html_element = soup.select_one('[itemprop="name"]')
name = name_html_element.get_text().strip()

git_branch_icon_html_element = soup.select_one('.octicon-git-branch')
main_branch_html_element = git_branch_icon_html_element.find_next_sibling('span')
main_branch = main_branch_html_element.get_text().strip()

# scrape the repo history data
boxheader_html_element = soup.select_one('.Box .Box-header')

relative_time_html_element = boxheader_html_element.select_one('relative-time')
latest_commit = relative_time_html_element['datetime']

history_icon_html_element = boxheader_html_element.select_one('.octicon-history')
commits_span_html_element = history_icon_html_element.find_next_sibling('span')
commits_html_element = commits_span_html_element.select_one('strong')
commits = commits_html_element.get_text().strip().replace(',', '')

# scrape the repo details in the right box
bordergrid_html_element = soup.select_one('.BorderGrid')

about_html_element = bordergrid_html_element.select_one('h2')
description_html_element = about_html_element.find_next_sibling('p')
description = description_html_element.get_text().strip()

star_icon_html_element = bordergrid_html_element.select_one('.octicon-star')
stars_html_element = star_icon_html_element.find_next_sibling('strong')
stars = stars_html_element.get_text().strip().replace(',', '')

eye_icon_html_element = bordergrid_html_element.select_one('.octicon-eye')
watchers_html_element = eye_icon_html_element.find_next_sibling('strong')
watchers = watchers_html_element.get_text().strip().replace(',', '')

fork_icon_html_element = bordergrid_html_element.select_one('.octicon-repo-forked')
forks_html_element = fork_icon_html_element.find_next_sibling('strong')
forks = forks_html_element.get_text().strip().replace(',', '')

# build the URL for README.md and download it
readme_url = f'https://raw.githubusercontent.com/luminati-io/luminati-proxy/{main_branch}/README.md'
readme_page = requests.get(readme_url)

readme = None
# if there is a README.md file
if readme_page.status_code != 404:
    readme = readme_page.text

# store the scraped data 
repo['name'] = name
repo['latest_commit'] = latest_commit
repo['commits'] = commits
repo['main_branch'] = main_branch
repo['description'] = description
repo['stars'] = stars
repo['watchers'] = watchers
repo['forks'] = forks
repo['readme'] = readme

# export the scraped data to a repo.json output file
with open('repo.json', 'w') as file:
    json.dump(repo, file, indent=4)