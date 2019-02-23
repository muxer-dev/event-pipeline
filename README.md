# Event Pipeline
An implementation of an events state machine using AWS Step Functions and the Serverless framework.

#### Linting

```sh
black src tests fixtures && isort -rc src tests fixtures
```

#### Testing

```sh
docker-compose build test && docker-compose run test
```

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

### Deploy

```sh
export AWS_ACCESS_KEY_ID=$(aws --profile muxer configure get aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws --profile muxer configure get aws_secret_access_key)

docker-compose build deploy && docker-compose run deploy
```
