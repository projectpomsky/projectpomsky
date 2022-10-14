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
  // The Pub/Sub message is passed as the CloudEvent's data payload.
  const base64name = cloudEvent.data.message.data;

  const name = base64name
    ? Buffer.from(base64name, 'base64').toString()
    : 'World';

  console.log(`Hello, ${name}!`);

  // Whenever this is invoked on a regular interval, it will either randomly show or hide my complaint 👇👇👇👇 (with a 3 to 1 odds of being hidden on any given day) 🤪
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

  console.log('github patch result =>', result?.status);

  return result;
});
// [END functions_cloudevent_pubsub]
