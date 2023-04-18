const fs = require('fs');

// Get the file name from command line argument
const fileName = process.argv[2];

// Read the JSON file
const data = fs.readFileSync(fileName);
const json = JSON.parse(data);

// Create a map to store the merged objects
const mergedObjects = new Map();

// Loop through each entry in the JSON
for (const key in json) {
  if (json.hasOwnProperty(key)) {
    const obj = json[key];
    // Check if the entry is an object
    if (typeof obj === 'object' && !Array.isArray(obj)) {
      // Extract the prefix from the key
      const prefix = key.split('_')[0];
      // If the prefix is not in the mergedObjects map, add it with the current object as value
      if (!mergedObjects.has(prefix)) {
        mergedObjects.set(prefix, obj);
      } else {
        // If the prefix is already in the mergedObjects map, merge the current object with the existing object
        const mergedObj = mergedObjects.get(prefix);
        mergedObjects.set(prefix, { ...mergedObj, ...obj });
      }
    }
  }
}

// Convert the merged objects from map to plain object
const mergedJson = Array.from(mergedObjects.entries()).reduce((acc, [key, value]) => {
  acc[key] = value;
  return acc;
}, {});

// Convert the merged JSON data to string
const mergedData = JSON.stringify(mergedJson, null, 2);

// Write the merged JSON data to a new file
fs.writeFileSync('mergedData.json', mergedData);

console.log('Merged JSON data has been written to mergedData.json');
