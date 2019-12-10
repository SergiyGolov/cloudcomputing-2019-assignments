#!/usr/bin/env bash
aws apigateway import-rest-api --body 'file://info_openapi_v2.yaml' > json_output

aws apigateway put-integration --rest-api-id `python3 extract_api_gateway_id.py` A PARTIR DE ICI --resource-id a1b2c3 --http-method GET --type AWS --integration-http-method POST --uri 'arn:aws:apigateway:us-west-2:lambda:path//2015-03-31/functions/arn:aws:lambda:us-west-2:123412341234:function:function_name/invocations'

rm json_output