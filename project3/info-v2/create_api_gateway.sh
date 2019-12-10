#!/usr/bin/env bash
aws apigateway import-rest-api --body 'file://info_openapi_v2.yaml' > json_output
aws lambda list-functions > lambda_info

aws apigateway get-resources --rest-api-id `python3 extract_api_gateway_id.py` > ressources_info

aws apigateway put-integration --rest-api-id `python3 extract_api_gateway_id.py` --resource-id `python3 extract_get_ressource_info.py` --http-method GET --type AWS_PROXY --integration-http-method POST --uri 'arn:aws:apigateway:eu-west-3:lambda:path/2015-03-31/functions/`python3 extract_lambda_arn.py`'

aws apigateway put-integration --rest-api-id `python3 extract_api_gateway_id.py` --resource-id `python3 extract_post_ressource_info.py` --http-method POST --type AWS_PROXY --integration-http-method POST --uri 'arn:aws:apigateway:eu-west-3:lambda:path/2015-03-31/functions/`python3 extract_lambda_arn.py`'

#rm json_output
#rm lambda_info
#rm ressources_info