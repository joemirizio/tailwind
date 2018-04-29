const fs = require('fs');
const path = require('path');
const esClient = require('./es');
const config = require('./config.json');

const dataDir = config.art.dataDir;

/**
 * Remove spaces in key names
 * @param {object} obj 
 * @return {object}
 */
function removeKeySpaces(obj) {
  for (key in obj) {
    if (obj.hasOwnProperty(key) && key.match(/ /)) {
      const val = obj[key];
      delete obj[key];
      obj[key.replace(/ /g, '')] = val;
    }
  }
  return obj;
}

/**
 * Index artwork 
 * @param {object} data Artwork data
 */
function indexArtwork(data) {
  esClient.deleteIndex();
  esClient.commitArtwork(data);
}

/**
 * Extract artwork from large JSON dump
 * @param {string} dataFile JSON file of all artwork
 * @param {string} outputFile Location to write extracted JSON
 * @param {*} filenames Filenames of artwork to extract
 */
function extractArtwork(dataFile, outputFile, filenames) {
  const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
  //indexArtwork(data);
  const selectedData = filenames
    .map(filename => data.filter(d => d['Image Filename'].startsWith(filename))[0])
    .map(art => removeKeySpaces(art));

  // Write art data
  fs.writeFileSync(outputFile, JSON.stringify(selectedData));
}

const dataFile = path.join(dataDir, config.art.collectionData);
const outputFile = path.join(dataDir, 'artwork.json');
const filenames = ["1929-184-16after-CX", "E1924-4-15v1-pma", "1958-132-1-CX", "E1945-1-1-pma2017", "1986-100-1-CX", "1978-100-1v1-ov", "1997-172-2"];
extractArtwork(dataFile, outputFile, filenames);