const fetch = require('node-fetch');
const retry = require('async-retry')

class PmaApiClient {

  constructor(token, uri = 'https://hackathon.philamuseum.org/api/v0') {
    this.token = token;
    this.baseUri = uri;
  }

  /**
   * Execute an API request with the API token
   * @param {string} endpoint API endpoint (e.g. 'collection/object')
   * @param {object} params Query parameters
   * @returns {Promise<object>} JSON response
   */
  async apiRequest(endpoint, params) {
    // Add API token to request
    params.api_token = this.token;

    // Build query
    const queryParams = [];
    for (const prop in params) {
      // TODO URL encode params
      queryParams.push(`${prop}=${params[prop]}`);
    }
    const queryString = queryParams.join('&');
    const query = `${this.baseUri}/${endpoint}?${queryString}`;

    try {
      // Need to retry because PMA API can sometimes return invalid responses
      return await retry(async bail => {
        const response = await fetch(query);
        return response.json();
      });
    } catch (e) {
      console.error(`Error fetching results for ${query}`, e);
    }
  }

  /**
   * Get all objects in the gallery
   * @param {number} id Gallery ID
   * @returns {Promise<Gallery>}
   */
  getObjectsByGallery(id) {
    const endpoint = 'collection/object/location'
    return this.apiRequest(endpoint, { name: id });
  }

  /**
   * Get object data
   * @param {number} id Object ID
   * @returns {Promise<Object>}
   */
  getObject(id) {
    const endpoint = 'collection/object';
    return this.apiRequest(endpoint, { query: id });
  }

}

module.exports = {
  PmaApiClient
};