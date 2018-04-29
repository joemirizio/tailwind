const fetch = require('node-fetch');

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

    const response = await fetch(query);
    return await response.json();
  }

  /**
   * Get all objects in the gallery
   * @param {number} id Gallery ID
   * @returns {Promise<Gallery>}
   */
  getObjectsByGallery(id) {
    const endpoint = 'collection/object/location'
    return apiRequest(endpoint, { name: id });
  }

  /**
   * Get object data
   * @param {number} id Object ID
   * @returns {Promise<Object>}
   */
  getObject(id) {
    const endpoint = 'collection/object';
    return apiRequest(endpoint, { query: id });
  }

}

module.exports = {
  PmaApiClient
};