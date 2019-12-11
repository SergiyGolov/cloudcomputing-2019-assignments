#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script is used to extract the ressource id of the get method for create_api_gateway.sh

import json

if __name__=='__main__':
    with open('./ressources_info') as f:
        text = f.read()
        json_output = json.loads(text)
        for d in json_output['items']:
            if d['path']=='/watch/{sku}':
                print(d['id'])