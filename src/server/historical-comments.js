// NODE_ENV == 'development':
//  fetch and return historical comments from live whimsy server
//  TODO: cache
// 
// NODE_ENV == 'production':
//   TODO

import credentials from './credentials.js';
import https from 'https';

export default async function historicalComments(request) {
  let { username, password } = credentials(request);

  return new Promise((resolve, reject) => {
    let options = {
      host: 'whimsy.apache.org',
      port: 443,
      path: '/board/agenda/json/historical-comments',
      headers: {
        'Authorization': 'Basic ' +
          Buffer.from(username + ':' + password).toString('base64')
      }
    };

    https.get(options, res => {
      let body = "";

      res.on('data', data => {
        body += data;
      });

      res.on('end', () => {
        resolve(body);
      });

      res.on('error', (error) => {
        reject(error)
      });
    });
  })
}