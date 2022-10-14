'use strict';

require('dotenv').config()
console.log(process.env) // remove this after you've confirmed it is working

import axios from 'axios';

const chance = require('chance').Chance();
const functions = require('@google-cloud/functions-framework');

// import * as dotenv from 'dotenv' // see https://github.com/motdotla/dotenv#how-do-i-use-dotenv-with-import
// dotenv.config()

const auth_header = `token ${process.env.GITHUB_TOKEN}`;

// Register a CloudEvent callback with the Functions Framework that will
// be executed when the Pub/Sub trigger topic receives a message from the Cloud Scheduler cron job.
functions.cloudEvent('helloPubSub', async cloudEvent => {

  // Whenever this is invoked on a regular interval, it will either randomly show or hide my complaint 👇👇👇👇 (with a 2 to 1 odds of being hidden on any given day) 🤪
  const randomFateOfRussiaVariable = chance.pick(["public", "private", "private"]) // 😜😜😜

  // It's in god's hands now.. 🙏🙏🙏🤭🤭🤭😊😊😊🤪
  const result = await axios.patch(`https://api.github.com/repos/projectpomsky/projectpomsky2`, {
    visibility: randomFateOfRussiaVariable
  }, {
    headers: {
      authorization: auth_header
    }
  });
  return result;
});
// [END functions_cloudevent_pubsub]