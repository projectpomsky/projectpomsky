const {getFunction} = require('@google-cloud/functions-framework/testing');
require('..');

describe('functions_cloudevent_pubsub', () => {
  const assert = require('assert');
  const uuid = require('uuid');
  const sinon = require('sinon');

  const stubConsole = function () {
    sinon.stub(console, 'error');
    sinon.stub(console, 'log');
  };

  const restoreConsole = function () {
    console.log.restore();
    console.error.restore();
  };

  beforeEach(stubConsole);
  afterEach(restoreConsole);

  it('should print a name from the pubsub message', () => {
    // Create mock Pub/Sub event
    const cloudEvent = {data: {message: {}}};
    const name = uuid.v4();
    cloudEvent.data.message = {
      data: Buffer.from(name).toString('base64'),
    };

    // Call tested function and verify its behavior
    const randomFateOfRussiaPubSub = getFunction('randomFateOfRussiaPubSub');
    randomFateOfRussiaPubSub(cloudEvent);
    assert.ok(console.log.calledWith(`Hello, ${name}!`));
  });

  it('randomFateOfRussiaPubSub: should print hello world', () => {
    // Create mock Pub/Sub event, in the event where a
    // PubSub message is empty but message has an attribute
    const cloudEvent = {data: {message: {data: null}}};

    // Call tested function and verify its behavior
    const randomFateOfRussiaPubSub = getFunction('randomFateOfRussiaPubSub');
    randomFateOfRussiaPubSub(cloudEvent);
    assert.ok(console.log.calledWith('Hello, World!'));
  });
});
