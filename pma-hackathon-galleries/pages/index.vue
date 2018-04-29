<template>
  <div class="app">
    <h1>PMA Hackathon Galleries</h1>
    <ol>
      <li v-for="(galleryId, i) in galleryIds" :key="galleryId" class="toc">
        <a :href="`#gallery-${i}`">{{ galleryObjects[i][0].Location.Gallery }}</a>
      </li>
    </ol>
    <div class="main-container">
      <div class="galleries">
        <section v-for="(galleryId, i) in galleryIds" :key="galleryId" class="gallery">
          <h2 :id="`gallery-${i}`">{{ galleryObjects[i][0].Location.Gallery }}</h2>
          <div class="artwork-container">
            <div v-for="artwork in galleryObjects[i]" :key="artwork.ObjectID" :id="`artwork-${artwork.ObjectID}`" :class="{'artwork': true, 'selected': recommendationArtwork.ObjectID === artwork.ObjectID}">
              <h3 @click="getRecommendations(artwork.ObjectID)">{{ artwork.Title }}</h3>
              <a :href="artwork.Image">
                <img :src="artwork.Thumbnail" :alt="artwork.Title"/>
              </a>
              <p>{{ artwork.Artist }}</p>
              <p>
                <small>
                {{ artwork.Classification }} • {{ artwork.Medium }} • {{ artwork.Dated }} • {{ artwork.Period }} • {{ artwork.Style }}
                </small>
              </p>
              <span v-for="socialTag in artwork.SocialTags" :key="socialTag" class="social-tag">
                {{ socialTag }}
              </span>
              <p>{{ artwork.GalleryLabel }}</p>
              <small>ID: {{ artwork.ObjectID }}</small>
            </div>
          </div>
        </section>
      </div>
      <div class="recommendations" v-if="recommendations.length > 0">
        <h2>Recommendations for {{ recommendationArtwork.Title }}</h2>
        <ul>
          <li v-for="artwork in recommendations" :key="artwork.ObjectID" class="recommendation">
            <a :href="`#artwork-${artwork.ObjectID}`">
              <img :src="artwork.Thumbnail" :alt="artwork.Title" />
              <p>{{ artwork.recommendation.weight }}</p>
              <p>{{ artwork.recommendation.description }}</p>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';

  const apiUri = process.env.API_URI || 'http://localhost:3001';
  
  export default {
    data() {
      return { 
        recommendationArtwork: '',
        recommendations: []
      };
    },
    methods: {
      findArtworkById(artworkId) {
        return this.galleryObjects.map(gallery => 
          gallery.filter(artwork => 
            artwork.ObjectID === artworkId
          )[0]
        ).filter(el => el)[0];
      },
      async getRecommendations(artworkId) {
        this.recommendationArtwork = this.findArtworkById(artworkId);

        const recommendations = (await axios.get(`${apiUri}/api/recommended/${artworkId}`)).data;
        this.recommendations = recommendations.map(recommendation => {
          const match = this.findArtworkById(recommendation.art_id);
          // Add recommendation data to matched artwork
          match.recommendation = recommendation;
          return match;
        });
      }
    },
    async asyncData({ params, error }) {
      try {
        const galleryIds = (await axios.get(`${apiUri}/api/galleries`)).data;
        const galleryIdParam = galleryIds.join(',');
        const galleryObjects = (await axios.get(`${apiUri}/api/galleryObjects/${galleryIdParam}`)).data;
        return { galleryIds, galleryObjects };
      } catch (e) {
        console.error(e);
        error({ statusCode: 400, message: e.message });
      }
    }
  };
</script>

<style scoped>
.app {
  font-family: 'Avenir', 'Helvetica', 'Arial', sans-serif;
  padding-left: 20px;
}

.main-container {
  display: flex;
  margin-top: 50px;
  height: 500px;
}

.galleries {
  flex: 1;
  overflow-y: scroll;
}

.artwork-container {
  display: grid;
  grid-gap: 20px;
  grid-template-columns: repeat(auto-fit, 300px);
}
.artwork {
  height: 200px;
  width: 250px;
  overflow: scroll;
  padding: 20px;
  background-color: #eee;
  transition: all 0.5s ease-in;
}
.artwork.selected {
  box-shadow: inset 10px 0 0 #e83a17;
}
.artwork:target {
  animation: pulse 1s;
}
@keyframes pulse {
  0% {
    background-color: #e83a17;
    color: white;
  }
  100% {
    background-color: #eee;
    color: inherit;
  }
}
.artwork h3 {
  margin-top: 0;
  cursor: pointer;
}
.artwork h3:hover {
  color: #e83a17;
}
.artwork img {
  height: 150px;
}
.artwork .social-tag {
  font-size: 0.7em;
  color: #333;
  background-color: white;
  border-radius: 5px;
  margin: 2px;
  padding: 2px 5px;
  display: inline-block;
}

.recommendations {
  width: 200px;
  padding: 20px;
  background-color: #eee;
  font-size: 0.7em;
  overflow-y: scroll;
}
.recommendations ul {
  padding-left: 0;
}
.recommendation {
  list-style: none;
  overflow: hidden;
}
.recommendation a {
  text-decoration: none;
}
.recommendations img {
  height: 100px;
  margin-top: 20px;
}
</style>