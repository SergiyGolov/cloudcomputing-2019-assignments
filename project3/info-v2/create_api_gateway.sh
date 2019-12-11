#!/usr/bin/env bash
aws apigateway import-rest-api --body 'file://info_openapi_v2.yaml' > json_output

aws lambda list-functions > lambda_info

aws apigateway create-deployment --region eu-west-3 \
    --rest-api-id `python3 extract_api_gateway_id.py` \
    --stage-name test

aws lambda add-permission \
    --function-name info-v2-dev \
    --action lambda:InvokeFunction \
    --statement-id lambda-invoke \
    --principal apigateway.amazonaws.com

aws apigateway get-resources --rest-api-id `python3 extract_api_gateway_id.py` > ressources_info

aws apigateway put-integration \
    --region eu-west-3 \
    --rest-api-id `python3 extract_api_gateway_id.py` \
    --resource-id `python3 extract_get_ressource_info.py` \
    --http-method GET \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri 'arn:aws:apigateway:eu-west-3:lambda:path/2012-10-17/functions/`python3 extract_lambda_arn.py`/invocations'

aws apigateway put-integration \
    --region eu-west-3 \
    --rest-api-id `python3 extract_api_gateway_id.py` \
    --resource-id `python3 extract_post_ressource_info.py` \
    --http-method POST \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri 'arn:aws:apigateway:eu-west-3:lambda:path/2012-10-17/functions/`python3 extract_lambda_arn.py`/invocations'

rm json_output
rm lambda_info
rm ressources_info
