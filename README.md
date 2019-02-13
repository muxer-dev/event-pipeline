# Event Pipeline
An implementation of an events state machine using AWS Step Functions and the Serverless framework.

#### Adds secrets to SSM parameter store

Prior to deploying changes you will need to add secret keys to the
[SSM Parameter Store](https://console.aws.amazon.com/systems-manager/parameters/?region=us-east-1);
This can be done via the UI or using the following commands (if you have the
relevant environment variables configured).

This creates the keys and values in the SSM parameter store:

```sh
aws ssm put-parameter --name meetupApiToken --region=eu-west-1 --type String --value ${MEETUP_API_TOKEN} --profile=muxer
```

This reads the keys and values from the SSM paramter store to ensure they have
been created successfully:

```sh
aws ssm get-parameters --region=eu-west-1 --name meetupApiToken --profile=muxer
```

### Manual Deployment

```sh
sls deploy --aws-profile=muxer --region-eu-west-1
```
