'use strict';

require('dotenv').config()
console.log(process.env) // remove this after you've confirmed it is working

import axios from 'axios';

const chance = require('chance').Chance();
const functions = require('@google-cloud/functions-framework');

const auth_header = `token ${process.env.GITHUB_TOKEN}`;

// Register a CloudEvent callback with the Functions Framework that will
// be executed when the Pub/Sub trigger topic receives a message.
functions.cloudEvent('helloPubSub', cloudEvent => {
  // The Pub/Sub message is passed as the CloudEvent's data payload.
  const base64name = cloudEvent.data.message.data;

  const name = base64name
    ? Buffer.from(base64name, 'base64').toString()
    : 'World';

  console.log(`Hello, ${name}!`);

  // on a regular interval when this is invoked, this will either randomly show or hide my complaint 👇👇👇👇, with a 2 to 1 odds of being hidden on any given day 🤪
  const randomFateOfRussiaVariable = chance.pick(["public", "private", "private"]) // 😜😜😜

  // it's in god's hands now.. 🤭🤭🤭😊😊😊🤪
  const result = axios.patch(`https://api.github.com/repos/projectpomsky/projectpomsky2`, {
    visibility:  randomFateOfRussiaVariable
  }, {
    headers: {
        authorization: auth_header
    }
});
return result;
});
// [END functions_cloudevent_pubsub]
