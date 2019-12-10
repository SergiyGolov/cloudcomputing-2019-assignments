#!/usr/bin/env bash
aws apigateway import-rest-api --body 'file://info_openapi_v2.yaml' > json_output
aws lambda list-functions > lambda_info

aws apigateway put-integration --rest-api-id `python3 extract_api_gateway_id.py` --resource-id `python3 extract_lambda_id.py` --http-method GET --type AWS_PROXY --integration-http-method POST --uri `python3 extract_lambda_arn.py`

rm json_output
rm lambda_info