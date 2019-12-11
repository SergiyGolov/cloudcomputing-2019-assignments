#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script is used to extract the lambda id for create_api_gateway.sh

import json

if __name__=='__main__':
    with open('./lambda_info') as f:
        text = f.read()
        json_output = json.loads(text)
        print(json_output['Functions'][0]['FunctionArn'].split(':')[-1])