const PmaApiCachingClient = require('./pma-api/PmaApiCachingClient');
const RecommendationEngine = require('./RecommendationEngine');

class HackathonServer {

  constructor(pgClient) {
    const apiToken = process.env.API_TOKEN;
    const cacheDir = process.env.CACHE_DIR;

    this.pmaClient = new PmaApiCachingClient(apiToken, cacheDir);
    this.recommendationEngine = new RecommendationEngine(pgClient);
  }

  async initialize() {
    try {
      const artworkData = await this.getArtworkFromGalleries(this.getGalleries());
      await this.recommendationEngine.initialize();
      await this.recommendationEngine.loadData(artworkData);
    } catch (e) {
      throw new Error(`Failed to initialize: ${e.message}`);
    }
  }

  getGalleries() {
    const galleryIds = [
      111, 116,
      155, 161,
      201, 204,
      226, 244,
      265
    ];
    return galleryIds;
  }

  async getArtworkFromGalleries(galleryIds) {
    return this.pmaClient.getObjectData(galleryIds);
  }

  async getRecommendedArtwork(artworkId) {
    const recommendations = await this.recommendationEngine.getRecommendedArtwork(artworkId);
    return recommendations.map(recommendation => {
      recommendation.description = this.recommendationEngine.getRecommendationDescription(recommendation)
      return recommendation;
    });
  }

}

module.exports = HackathonServer;