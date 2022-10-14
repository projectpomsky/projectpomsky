const supertest = require('supertest');
const functionsFramework = require('@google-cloud/functions-framework/testing');

require('../index');

describe('functions_cloudevent_pubsub', () => {
  it('should process a CloudEvent', async () => {
    const cloudEventData = {data: {message: {}}};

    const name = 'Cecil';
    cloudEventData.data.message = {
      data: Buffer.from(name).toString('base64'),
    };

    const server = functionsFramework.getTestServer('randomFateOfRussiaPubSub');
    await supertest(server)
      .post('/')
      .send(cloudEventData)
      .set('Content-Type', 'application/json')
      .expect(204);
  });
});
