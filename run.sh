# Create cloud scheduler cron job which is currently set to invoke the helloPubSub topic once at 4:05am daily, 
# which in turn will randomly either show or hide my complaint with 2 to 1 odds of it being hidden on any given day as shown in the index.js file 🤪🤪🤪
gcloud beta scheduler jobs create pubsub startup-dev-instances \
  --schedule '5 4 * * *' \
  --topic helloPubSub \
  --message-body '{"zone":"us-west1-b", "label":"env=dev"}' \
  --location nodejs-pubsub-function-832534

# Start cloud scheduler cron job
gcloud beta scheduler jobs run startup-dev-instances

# Show logs of cloud scheduler cron job
gcloud compute instances describe dev-instance \
--zone us-west1-b \
| grep status
