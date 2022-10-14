'use strict';

require('dotenv').config()
console.log(process.env)

const axios = require('axios');
const chance = require('chance').Chance();
const functions = require('@google-cloud/functions-framework');
const auth_header = `token ${process.env.GITHUB_TOKEN}`;

// Register a CloudEvent callback with the Functions Framework that will
// be executed when the Pub/Sub trigger topic receives a message from the Cloud Scheduler cron job.
functions.cloudEvent('randomFateOfRussiaPubSub', async cloudEvent => {

  // Whenever this is invoked on a regular interval, it will either randomly show or hide my complaint 👇👇👇👇 (with a 2 to 1 odds of being hidden on any given day) 🤪
  const randomFateOfRussiaVariable = chance.pickone(["public", "private", "private"]) // 😜😜😜

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
