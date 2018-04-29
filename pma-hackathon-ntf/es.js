const elasticsearch = require('elasticsearch');
const config = require('./config.json');

const client = new elasticsearch.Client({
  host: config.es.host,
  log: config.es.logLevel,
});

function getItemByFilename(id, cb) {
  client.search({
    index: config.es.index,
    size: 1,
    q: `Image Filename:${id}`
  }, cb);
}

function getPaintingFilenames(cb) {
  client.search({
    index: config.es.index,
    size: config.es.resultsSize,
    q: 'Classification:Paintings',
    _source: ['ObjectID', 'Image Filename']
  }, cb);
}

function deleteIndex() {
  client.delete({
    index: config.es.index
  });
}

function commitArtwork(data) {
  const commit = [];
  data.forEach(d => {
    commit.push({
      index:  {
        _index: config.es.index,
        _type: 'artwork',
        _id: d.ObjectID
      }
    });
    commit.push(d);
  });
  client.bulk({
    body: commit
  }, (err, resp) => {
    if (err) {
      console.error(error);
      return;
    }
    console.debug(`Committed ${resp.items.length} items in ${resp.took}ms`);
  });
}

module.exports = {
  getItemByFilename,
  getPaintingFilenames,
  deleteIndex,
  commitArtwork
}
