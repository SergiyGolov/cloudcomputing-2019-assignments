#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

if __name__=='__main__':
    with open('./ressources_info') as f:
        text = f.read()
        json_output = json.loads(text)
        for d in json_output['items']:
            if d['path']=='/watch':
                print(d['id'])