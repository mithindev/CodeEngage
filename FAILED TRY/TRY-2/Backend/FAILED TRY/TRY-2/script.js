const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Replace 'YOUR_PERSONAL_ACCESS_TOKEN' with your actual PAT
const PERSONAL_ACCESS_TOKEN = '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';

// Define your User-Agent
const user_agent = 'GitHub Repository Scraper';

async function scrapeGitHubRepository(repoUrl, outputDir = '') {
  // Extract owner and repository name from the URL
  const urlParts = repoUrl.split('/');
  const repoOwner = urlParts[urlParts.length - 2];
  const repoName = urlParts[urlParts.length - 1];

  // GitHub API endpoint to get repository contents
  const apiURL = `https://api.github.com/repos/${repoOwner}/${repoName}/contents`;

  // Make a GET request to the API endpoint with authentication
  const headers = {
    'Authorization': `Bearer ${PERSONAL_ACCESS_TOKEN}`,
    'User-Agent': user_agent
  };

  try {
    const response = await axios.get(apiURL, { headers });

    if (response.status === 200) {
      const contents = response.data;

      // Create the output directory if it doesn't exist
      if (outputDir) {
        fs.mkdirSync(outputDir, { recursive: true });
      }

      // Loop through each item in the contents
      for (const item of contents) {
        if (item.type === 'file') {
          const fileUrl = item.download_url;
          const fileName = item.name;

          // Make a GET request to download the file content
          const fileResponse = await axios.get(fileUrl, { headers });

          if (fileResponse.status === 200) {
            const fileContent = fileResponse.data;

            // Determine the file path in the output directory
            const filePath = path.join(outputDir, fileName);

            // Write the content to the file
            fs.writeFileSync(filePath, fileContent);
          } else {
            console.log(`Failed to download ${fileName}`);
          }
        } else if (item.type === 'dir') {
          // Recursively scrape the contents of subfolders
          const folderUrl = item.url.replace('/repos', '');
          const folderName = item.name;
          const subdirOutputDir = path.join(outputDir, folderName);

          console.log(`Folder Link: ${folderUrl}`);
          await scrapeGitHubRepository(folderUrl, subdirOutputDir);
        }
      }

      console.log('Repository content scraped and saved.');
    } else {
      console.log('Failed to fetch repository contents.');
    }
  } catch (error) {
    console.error(error.message);
  }
}

// Example usage
const repositoryUrl = 'https://github.com/mithindev/COLLEGE';
scrapeGitHubRepository(repositoryUrl, 'output_folder');
