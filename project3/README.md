Cloud Computing Project 3 - Serverless Webservice
===

Goloviatinski Sergiy

Herbelin Ludovic

## State of the project

The project was almost completed, up until the automated API gateway deployment. The scripts to create the lambdas are functional but the one for the API gateway creates it but cannot bind the lambdas functions to it.

We created some python scripts to extract some information we needed to provide to the aws CLI commands but we could not find the correct structure of the uri for the `aws apigateway put-integration` command.

Note : We disabled the HTTP basic auth because it caused some issues, as user was never prompted to give credentials. It might be because the HTTP WWW-authenticate header is not included in the responses.

## Deployment

First of all, if not done already, you need to setup your aws config on your local machine. You need to have the `awscli` python module installed, as described on https://github.com/aws/aws-cli .

Then you need to configure your aws credentials and setup the general configuration using the command `aws configure`. You need to have your access and secret access keys generated (see https://docs.aws.amazon.com/fr_fr/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys).

Then for the project's setup we strongly suggest creating a virtualenv for example :

- `cd info-v2`
- `virtualenv -p python3 venv`
- `pip install -r requirements.txt` 

Then you are ready to deploy. Here are the scripts you need to execute in order :

- `./initialize_dynamodb.sh`
- `./create_lambdas.sh`
- `./create_api_gateway.sh`

The script `./update_lambdas.sh` is provided to use once the lambdas were created if the code was modified.


## Testing

You can either test it using the endpoint in your browser :
https://2w8ug39859.execute-api.eu-west-3.amazonaws.com/dev/info/v2/watch/CAC1111.BT0705

Or using a curl command : `curl -X POST "https://2w8ug39859.execute-api.eu-west-3.amazonaws.com/dev/info/v2/watch" -H "accept: /" -H "Content-Type: application/json" -d`

Both should return JSON values such as : 
```json
{"sku":"striiiiiiing","type":"watchOSS","status":"old","gender":"man","year":0,"dial_material":"string","dial_color":"string","case_material":"string","case_form":"string","bracelet_material":"string","movement":"string"}"
```

Note : HTTP basic auth was removed as it caused some issues with the AWS lambda, it never asked for the authentication and just returned a HTTP 401 Unauthorized error. Thus, you don't have to input credentials.