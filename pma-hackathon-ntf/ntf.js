const fs = require("fs");
const util  = require('util');
const spawn = require('child_process').spawn;
const spawnSync = require('child_process').spawnSync;
const sleep = require('sleep');
const esClient = require('./es');
const config = require('./config.json');

const dataDirectory = `${config.art.mediaDir}/Full_Res`;
const artoolkitDirectory = config.ar.artoolkitDir;
const genTexData = `${artoolkitDirectory}/bin/genTexData`;
const genTexDataArgs = config.ar.genTexDataArgs;

function filenameWithoutExtension(filepath) {
  const filename = filepath.substring(0, filepath.lastIndexOf('/'));
  return filename.substring(0, filename.lastIndexOf('.'));
}

function generateNtfData(directory, filenames) {
  const markers = [];
  const filepaths = filenames.map(filename => `${directory}/${filename}`);
  const numFiles = filepaths.length;

  filepaths.forEach((filepath, i) => {
    const args = [...genTexDataArgs, filepath];

    console.log(`${i}/${numFiles} ${filepath}`);
    //console.log(genTexData, args.join(' '));
    const cmd = spawnSync(genTexData, args);
    //cmd.stdout.on('data', d => console.log(d));
    //cmd.stderr.on('data', d => console.error(d));
    //cmd.on('exit', code => next = true);

    /*if (i > 0 && i % 20 === 0) {
      sleep.sleep(60 * 5);
    }*/

    const filename = filenameWithoutExtension(filepath);
    markers.push(`${filename}\nNFT\n`);
  });

  // Write markers.dat
  const markerContents = `${markers.length}\n\n${markers.join('\n')}`;
  fs.writeFile(`${directory}/markers.dat`, markerContents, (err) => {
    if (err) {
      console.log(err);
    }
  });
}

esClient.getPaintingFilenames((err, resp) => {
  //const filenames = resp.hits.hits.map(obj => obj._source['Image Filename']);
  const filenames = ['1997-172-2.jpg'];
  generateNtfData(dataDirectory, filenames);
});
