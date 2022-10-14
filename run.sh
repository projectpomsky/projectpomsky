# Set gcloud project
gcloud config set project project-pomsky-123

# Create pub-sub topic
gcloud pubsub topics create randomFateOfRussiaPubSub

# Publish the google cloud function
gcloud functions deploy projectpomsky-show-hide-pub-sub-function --gen2 \
--runtime=nodejs16 \
--region=us-west1 \
--source=. \
--entry-point=randomFateOfRussiaPubSub \
--trigger-topic=randomFateOfRussiaPubSub

# Create cloud scheduler cron job which is currently set to invoke the randomFateOfRussiaPubSub topic once at 4:05am daily, 
# which in turn will randomly either show or hide my complaint with 2 to 1 odds of it being hidden on any given day, as shown in the index.js file 🤪🤪🤪
gcloud beta scheduler jobs create pubsub random-fate-of-russia-cron-job \
  --schedule '5 4 * * *' \
  --topic randomFateOfRussiaPubSub \
  --message-body '{"zone":"us-west1-b", "label":"env=dev"}' \
  --location nodejs-pubsub-function-832534

# Start cloud scheduler cron job
gcloud beta scheduler jobs run random-fate-of-russia-cron-job

# Show logs of cloud scheduler cron job
gcloud compute instances describe random-fate-of-russia-cron-job \
--zone us-west1-b \
| grep status

# 🤭🤭🤭