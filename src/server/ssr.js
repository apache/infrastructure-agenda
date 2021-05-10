import { promises as fs } from "fs";
import path from 'path';
import { renderToString } from 'react-dom/server';
import { Provider } from 'react-redux';
import { StaticRouter } from 'react-router-dom';
import Router from '../client/router.js';
import React from "react";
import store, { setCache } from '../client/store.js';
import * as Actions from "../actions.js";
import * as cache from "./cache.js";
import server from './sources/server.js';

// server side rendering of content.  Speeds up the initial display when first
// navigating to a page, opening a page in a new tab, or (depending on the
// browser) hitting the back button to return to a page inside the app from
// one outside the app.

export default async function ssr(request, response) {
  let html = await fs.readFile(path.join(__dirname, '../../build', 'index.html'), 'utf8');

  store.dispatch(Actions.postServer(await server(request)));

  try {
    const context = {};
    const app = renderToString(
      <Provider store={store}>
        <StaticRouter location={request.url} context={context}>
          <Router />
        </StaticRouter>
      </Provider>
    );

    let state = JSON.stringify(store.getState());

    html = html.replace(
      '<div id="root"></div>',
      `<div id="root">${app}</div><script>window.REDUX_STATE=${state}</script>`
    );
  } catch {
  }

  response.setHeader('content-type', 'text/html; charset=utf-8');
  response.send(html);
}

// provide store with access to the server cache
setCache(path => cache.values[path]);
