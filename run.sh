# create cloud scheduler cron job, currently set to be run once at 4:05am daily, however there
# is two-to-one odds the repository will remain hidden for the day given the chance.js logic 🤪🤪🤪
gcloud beta scheduler jobs create pubsub startup-dev-instances \
  --schedule '5 4 * * *' \
  --topic helloPubSub \
  --message-body '{"zone":"us-west1-b", "label":"env=dev"}' \
  --location nodejs-pubsub-function-832534

# start cloud scheduler cron job
gcloud beta scheduler jobs run startup-dev-instances

# show logs of cloud scheduler cron job
gcloud compute instances describe dev-instance \
--zone us-west1-b \
| grep status
