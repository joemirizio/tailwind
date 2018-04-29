const express = require('express');
const cors = require('cors')
const { Client } = require('pg');
const HackathonServer = require('./HackathonServer');

require('dotenv').config();
const port = process.env.API_PORT;

const app = express();

// Postgres client
const pgClient = new Client();
// FIXME Should await the connection
pgClient.connect();

const hackathonServer = new HackathonServer(pgClient);

app.use(cors());
app.use('/api/initialize', async (req, res) => {
  try {
    await hackathonServer.initialize();
    res.send('Initialized');
  } catch (e) {
    res.status(500).send(e.message);
  }
});
app.use('/api/galleries', (req, res) => {
  const galleryIds = hackathonServer.getGalleries();
  res.send(JSON.stringify(galleryIds));
});
app.use('/api/galleryObjects/:galleryIds', async (req, res) => {
  const galleryIds = req.params.galleryIds.split(',').map(val => parseInt(val, 10));
  const objectData = await hackathonServer.getArtworkFromGalleries(galleryIds);
  res.send(JSON.stringify(objectData));
});
app.use('/api/recommended/:artworkId', async (req, res) => {
  const recommendedArtwork = await hackathonServer.getRecommendedArtwork(req.params.artworkId);
  res.send(JSON.stringify(recommendedArtwork));
});

app.listen(port, () => console.log(`Server listening on port ${port}!`));