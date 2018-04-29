class RecommendationEngine {

  constructor(pgClient) {
    this.client = pgClient;
  }

  async initialize() {
    const createTableResult = await this.client.query(`
      DROP TABLE IF EXISTS ARTWORK_DATA;
      CREATE TABLE IF NOT EXISTS ARTWORK_DATA (
        id SERIAL,
        art_id int,
        key varchar(50),
        value varchar(100),
        weight int
      );`);
  }

  async loadData(artworkData) {
    const fields = [
      'Location.GalleryShort', 'Location.Gallery', 'Artists.Artist', 'Classification', 
      'Style', 'Movement', 'DateBegin', 'Period', 'School', 'Dynasty', 
      'Reign', 'SocialTags'
    ].reverse();
    artworkData.forEach(gallery => {
      gallery.forEach(artwork => {
        fields.forEach((key, i) => {
          let keyB;
          if (key.indexOf('.') > -1) {
            [key, keyB] = key.split('.');
          }
          if (artwork.hasOwnProperty(key) && artwork[key]) {
            const artworkId = parseInt(artwork.ObjectID, 10)
            let values = artwork[key];
            if (Object.prototype.toString.call(values) !== '[object Array]') {
              values = [values];
            }
            values.forEach(async value => {
              if (keyB) {
                key = keyB;
                value = value[keyB];
                // Transform the full gallery label into the wing
                if (keyB === 'Gallery') {
                  key = 'Wing'
                  value = value.split(', ')[1];
                }
              }
              const weight = 2 ** (i + 1);
              const preparedValues = [artworkId, key, value, weight];
              try {
                await this.client.query(`
                  INSERT INTO ARTWORK_DATA(art_id, key, value, weight) 
                  VALUES($1, $2, $3, $4)`, preparedValues);
              } catch (e) {
                console.error(`Failed to insert values ${preparedValues}`, e);
              }
            });
          }
        });
      });
    });
  }

  async getRecommendedArtwork(id) {
    const res = await this.client.query(`
      SELECT 
        B.art_id, 
        string_agg(replace(B.key, '|', '.'), '|' ORDER BY B.weight DESC) as reason, 
        string_agg(replace(B.value, '|', '.'), '|' ORDER BY B.weight DESC) as rationale, 
        SUM(B.weight) as weight
      FROM ARTWORK_DATA A
      JOIN ARTWORK_DATA B ON A.key = B.key
      WHERE
        A.art_id = $1 AND 
        A.value = B.value AND
        B.art_id != A.art_id
      GROUP BY B.art_id
      ORDER BY weight DESC;
    `, [id]);
    return res.rows;
  }

  getRecommendationDescription(recommendation) {
    const reasons = recommendation.reason.split('|');
    const rationales = recommendation.rationale.split('|');
    let messages = [];

    reasons.forEach((reason, i)=> {
      const rationale = rationales[i];
      const rationaleLowerCase = rationale.toLowerCase();
      const rationalePlural = /s$/.test(rationaleLowerCase) ? '' : 's';
      switch (reason) {
        case 'GalleryShort':
          messages.push('located in the same gallery');
          break;
        case 'Wing':
          if (!reasons.includes('GalleryShort')) {
            messages.push('located in the same wing');
          }
        case 'Classification':
          // TODO Add appropriate pluralization
          messages.push(`are both ${rationaleLowerCase}${rationalePlural}`);
          break;
        case 'Style':
          messages.push(`both in the ${rationaleLowerCase} style`);
          break;
        case 'Movement':
          messages.push(`in the ${rationale} movement`);
        case 'SocialTags':
          messages.push(`have to do with ${rationale}`);
          break;
      }
    });

    // Add 'and'
    if (messages.length > 1) {
      messages[messages.length - 1] = 'and ' + messages[messages.length - 1];
    }

    const message = (messages.length > 2) ? messages.join(', ') : messages.join(' ');
    return 'These pieces are ' + message;
  }

}

module.exports = RecommendationEngine;
