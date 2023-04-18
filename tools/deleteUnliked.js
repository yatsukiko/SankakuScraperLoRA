const fs = require('fs');
const path = require('path');

const directoryPath = process.argv[2]; // get directory path from command line argument
const allowedExtensions = ['.jpg', '.png', '.gif'];

if (!directoryPath) {
  console.error('Please provide a directory path as an argument.');
  process.exit(1);
}

fs.readdir(directoryPath, (err, files) => {
  if (err) {
    console.error('Error reading directory: ', err);
    return;
  }

  files.forEach((file) => {
    const extension = path.extname(file);
    const basename = path.basename(file, extension);

    if (extension === '.txt') {
      const imageFileExists = allowedExtensions.some((ext) =>
        fs.existsSync(path.join(directoryPath, basename + ext))
      );

      if (!imageFileExists) {
        fs.unlinkSync(path.join(directoryPath, file));
        console.log(`Deleted ${file}`);
      }
    }
  });
});
