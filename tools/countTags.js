const fs = require('fs');
const path = require('path');

const folderPath = process.argv[2]; // Get folder path from command-line argument

if (!folderPath) {
  console.error('Usage: node tag_frequency.js [folder_path]');
  process.exit(1);
}

const tagFrequency = {};

fs.readdir(folderPath, (err, files) => {
  if (err) {
    console.error(err);
    return;
  }

  files.forEach((file) => {
    const extension = path.extname(file);
    if (extension === '.txt') {
      const filePath = path.join(folderPath, file);
      const fileContent = fs.readFileSync(filePath, 'utf-8');
      const tags = fileContent.split(',').map((tag) => tag.trim());

      tags.forEach((tag) => {
        if (tag in tagFrequency) {
          tagFrequency[tag]++;
        } else {
          tagFrequency[tag] = 1;
        }
      });
    }
  });

  const sortedTags = Object.entries(tagFrequency)
    .sort((a, b) => b[1] - a[1])
    .reduce((acc, [tag, count]) => ({ ...acc, [tag]: count }), {});

  const jsonOutput = JSON.stringify(sortedTags, null, 2);
  const outputFile = path.join(folderPath, 'tag_frequency.json');
  fs.writeFileSync(outputFile, jsonOutput);
});
