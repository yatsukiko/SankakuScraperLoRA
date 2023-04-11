const fs = require('fs');
const prompt = require('prompt-sync')();
const https = require('https');
const datasetFolder = 'dataset/'; 
//setup user agent, otherwise we get unauthorized
const options = {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
  };

// setup, ask for .json file name and dataset name
var resFile = prompt('Enter Octoparse json result filename (Default: "chan.sankakucomplex Scraper.json"): ') || "chan.sankakucomplex Scraper.json";
//loop if empty
while (!fs.existsSync(resFile)) {
  console.log('File not found!');
  resFile = prompt('Enter Octoparse json result filename (Default: "chan.sankakucomplex Scraper.json"): ') || "chan.sankakucomplex Scraper.json";
}
var datasetName = prompt('Enter dataset name (requierd): ');
//loop if empty
while (!datasetName) {
    datasetName = prompt('Enter dataset name (requierd): ');
}
//confirm selection
console.log(`File found: ${resFile}`);

//parse json then pretty print and remove empty img_src
const data = fs.readFileSync(resFile, {encoding:'utf8', flag:'r'});
const json = JSON.parse(data);
const filteredJson = json.filter(obj => obj.img_src !== "");
const prettyJson = JSON.stringify(filteredJson, null, 2);
// save pretty printed + filtered json
fs.writeFile(resFile, prettyJson, err => {
    if (err) {
        console.error(err);
        return;
    }
console.log(`Successfully pretty-printed and saved ${resFile}`);
//download image function, uses user agent + check for status code
const downloadImage = (url, destination) => {
  return new Promise((resolve, reject) => {
    https.get(url, options, response => {
      if (response.statusCode !== 200) {
        reject(new Error(`Failed to download ${url}. Status code: ${response.statusCode}`));
      } else {
        const file = fs.createWriteStream(destination);
        response.pipe(file);
        file.on('finish', () => {
          file.close(resolve);
          console.log("Downloaded " + url);
        });
        file.on('error', error => {
          fs.unlink(destination, () => {
            reject(error);
          });
        });
      }
    }).on('error', error => {
      fs.unlink(destination, () => {
        reject(error);
      });
    });
  });
};

  
  //download all img_src entries, and if it fails try again up to x times
  const retryDownloadImage = (url, destination, retriesLeft) => {
    return downloadImage(url, destination).catch(error => {
      if (retriesLeft === 0) {

        throw error;
      }
      console.log(`Retrying download of ${url}. Retries left: ${retriesLeft}`);
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(retryDownloadImage(url, destination, retriesLeft - 1));
        }, 1000);
      });
    });
  };
  
  
  const main = async () => {
    const numImages = filteredJson.length;
    //create dataset folder name and figure out steps
    if (1500/numImages < 100){
        var steps = 100 + `_${datasetName}/`
    } else {
        var steps = Math.round(1500/numImages) + `_${datasetName}/`
    }
    const subDatasetFolder = datasetFolder + steps 
    if (!fs.existsSync(datasetFolder)) {
        fs.mkdirSync(datasetFolder);
      }
    if (!fs.existsSync(subDatasetFolder)) {
        fs.mkdirSync(subDatasetFolder);
      }
    //download all img_src and rename them, try 5 time if it fails
    for (let i = 0; i < numImages; i++) {
      const image = filteredJson[i];
      const ext = image.img_src.split('.').pop().split('?')[0];
      const destination = `${subDatasetFolder}${i}.${ext}`;
      try {
        await retryDownloadImage(image.img_src, destination, 5);
      } catch (error) {
        console.log(`Failed to download ${image.img_src}: ${error.message}`);
        continue;
      }
      //write a corresponding .txt with img_tags next to it.
      const tags = image.img_tags.split(" ");
      const formattedTags = tags.join(", ");
      const txtDestination = `${subDatasetFolder}${i}.txt`;
      fs.writeFileSync(txtDestination, formattedTags);
    }
    console.log('Done!');
  };
  
  main().catch(error => {
    console.log(`Error: ${error.message}`);
    process.exit(1);
  });


});