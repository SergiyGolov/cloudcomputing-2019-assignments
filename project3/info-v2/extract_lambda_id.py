#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

if __name__=='__main__':
    with open('./lambda_info') as f:
        text = f.read()
        json_output = json.loads(text)
        print(json_output['Functions'][0]['FunctionArn'].split(':')[-1])