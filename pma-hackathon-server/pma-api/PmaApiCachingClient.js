const fs = require('fs');
const path = require('path');
const util = require('util');
const { PmaApiClient } = require('./PmaApiClient');

const readFilePromise = util.promisify(fs.readFile);

class PmaApiCachingClient {

  constructor(apiToken, cacheDir) {
    this.pma = new PmaApiClient(apiToken);
    this.cacheDir = cacheDir;
  }

  /**
   * Generate a filename for a gallery
   * @param {string} galleryShort Gallery short name (e.g. 'Gallery 111')
   */
  generateGalleryFileName(galleryShort) {
    return galleryShort.replace(' ', '-').toLowerCase() + '.json';
  }

  /**
   * Load/cache gallery data for given galleries from the cache or API
   * @param {number[]} galleryIds Gallery IDs
   * @returns {Promise<Gallery>} Gallery data
   */
  async loadGalleryData(galleryIds) {
    let galleryObjects;

    const galleryObjectsFile = path.join(this.cacheDir, 'galleryObjects.json');
    if (!fs.existsSync(galleryObjectsFile)) {
      try {
        // Fetch gallery data
        galleryObjects = await Promise.all(galleryIds.map(gallery => 
          this.pma.getObjectsByGallery(gallery)
        ));
        // Cache results
        fs.writeFile(galleryObjectsFile, JSON.stringify(galleryObjects), () =>
          console.debug(`Wrote ${galleryObjectsFile} to cache`)
        );
      } catch (e) {
        console.error('Failed to read gallery data', e);
      }
    } else {
      // Load gallery data from cache
      galleryObjects = JSON.parse(await readFilePromise(galleryObjectsFile))
        .filter(gallery => galleryIds.includes(parseInt(gallery.GalleryShort.replace('Gallery ', ''), 10)));
    }

    return galleryObjects;
  }

  /**
   * Get object data
   * @param {Gallery[]} galleries Array of Gallery objects
   * @returns {Promise<Object>} Object data
   */
  async loadObjectData(galleries) {
    return Promise.all(galleries.map(async gallery => {
      const galleryName = gallery.GalleryShort;
      const galleryFile = path.join(this.cacheDir, this.generateGalleryFileName(galleryName));
      let objectData;
      if (!fs.existsSync(galleryFile)) {
        // Fetch object data
        console.debug(`Fetching ${galleryName} from API`);
        try {
          objectData = await Promise.all(gallery.ObjectIDs.map(id => this.pma.getObject(id)));
          // Cache results
          fs.writeFile(galleryFile, JSON.stringify(objectData), () =>
            console.debug(`Wrote ${galleryFile} to cache`)
          );
        } catch (e) {
          console.error(`Failed to read ${galleryName} data`, e);
        }
      } else {
        // Load object data from cache
        console.debug(`Fetching ${galleryName} from cache`);
        objectData = JSON.parse(await readFilePromise(galleryFile));
      }
      return objectData;
    }));
  }

  async getObjectData(galleryIds) {
    const galleryObjects = await this.loadGalleryData(galleryIds, this.cacheDir);
    const galleryObjectData = await this.loadObjectData(galleryObjects, this.cacheDir);
    return galleryObjectData;
  }

  generateTagMap(galleryObjectData) {
    const tagMap = new Map();
    galleryObjectData.forEach(gallery => 
      gallery.forEach(obj => {
        if (obj.SocialTags) {
          obj.SocialTags.forEach(tag => {
            tagMap.set(tag, tagMap.has(tag) ? tagMap.get(tag) + 1 : 1);
          });
        }
      })
    );
    return tagMap;
  } 

}

module.exports = PmaApiCachingClient;