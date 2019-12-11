#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# THis script is used to extract teh api gateway id for create_api_gateway.sh

import json

if __name__=='__main__':
    with open('./json_output') as f:
        text = f.read()
        json_output = json.loads(text)
        print(json_output['id'])