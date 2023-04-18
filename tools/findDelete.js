const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2); // Get command-line arguments
const directory = args[0]; // First argument is the path to the image directory
const keyword = args[1]; // Second argument is the keyword to search for

const rejectedFolder = path.join(directory, 'rejected');
if (!fs.existsSync(rejectedFolder)) {
  fs.mkdirSync(rejectedFolder);
}

fs.readdir(directory, (err, files) => {
  if (err) throw err;

  // Loop through all the files in the directory
  files.forEach(file => {
    const extension = path.extname(file);
    if (extension === '.txt') {
      const txtFilePath = path.join(directory, file);
      fs.readFile(txtFilePath, 'utf8', (err, data) => {
        if (err) throw err;

        // Parse the tags as an array
        const tags = data.split(',').map(tag => tag.trim());

        // Check if any tag contains the keyword
        if (tags.includes(keyword)) {
          // Move the corresponding image file to the rejected folder
          const imgExtensions = ['.jpg', '.png', '.gif'];
          const imgExtension = imgExtensions.find(ext => fs.existsSync(path.join(directory, file.replace('.txt', ext))));
          if (imgExtension) {
            const imgFilePath = path.join(directory, file.replace('.txt', imgExtension));
            const rejectedImgFilePath = path.join(rejectedFolder, path.basename(imgFilePath));
            fs.rename(imgFilePath, rejectedImgFilePath, err => {
              if (err) throw err;
              console.log(`Moved ${imgFilePath} to ${rejectedImgFilePath}`);
            });
          }

          // Move the text file to the rejected folder
          const rejectedTxtFilePath = path.join(rejectedFolder, file);
          fs.rename(txtFilePath, rejectedTxtFilePath, err => {
            if (err) throw err;
            console.log(`Moved ${txtFilePath} to ${rejectedTxtFilePath}`);
          });
        }
      });
    }
  });
});
