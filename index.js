'use strict';

require('dotenv').config()
console.log(process.env)

const axios = require('axios');
const chance = require('chance').Chance();
const functions = require('@google-cloud/functions-framework');
const authHeader = `token ${process.env.GITHUB_TOKEN}`;

console.log('authHeader =>', authHeader);

// Register a CloudEvent callback with the Functions Framework that will
// be executed when the Pub/Sub trigger topic receives a message from the Cloud Scheduler cron job.
functions.cloudEvent('randomFateOfRussiaPubSub', async cloudEvent => {

  // Whenever this is invoked on a regular interval, it will either randomly show or hide my complaint 👇👇👇👇 (with a 2 to 1 odds of being hidden on any given day) 🤪
  const randomFateOfRussiaVariable = chance.pickone(["private", "private", "private", "public"]) // 😜😜😜

  // Log what was decided
  console.log('randomFateOfRussiaVariable =>', randomFateOfRussiaVariable);

  // It's in god's hands now.. 🙏🙏🙏😉🤭🤭🤭😊😊😊🤪
  const result = await axios.patch(`https://api.github.com/repos/projectpomsky/projectpomsky2`, {
    visibility: randomFateOfRussiaVariable
  }, {
    headers: {
      "authorization": authHeader,
      "Content-Type": "application/json"
    }
  });

  console.log('github patch result =>', result);

  return result;
});
// [END functions_cloudevent_pubsub]
