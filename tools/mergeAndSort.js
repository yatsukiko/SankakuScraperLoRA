const fs = require('fs');

// Get the file name from command line argument
const fileName = process.argv[2];

// Read the JSON file
const data = fs.readFileSync(fileName);
const json = JSON.parse(data);

// Concatenate all objects into one object
const combinedObj = Object.assign({}, ...Object.values(json));

// Sort the combined object by values in descending order
const sortedObj = Object.entries(combinedObj)
  .sort(([, a], [, b]) => b - a)
  .reduce((acc, [k, v]) => {
    acc[k] = v;
    return acc;
  }, {});

// Write the sorted JSON data to a new file
fs.writeFileSync('sortedData.json', JSON.stringify(sortedObj, null, 2));

console.log('Sorted JSON data has been written to sortedData.json');
