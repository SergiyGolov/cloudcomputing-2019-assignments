#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

if __name__ == '__main__':
    with open('./db/watches.json') as f:
        text = f.read()
        old_json = json.loads(text)
        new_json = {'watches': []}
        for watch in old_json:
            d = {
                'PutRequest':
                {
                    'Item': {}
                }
            }
            for k, v in watch.items():
                if v == None:
                    continue
                if k != 'year':
                    d['PutRequest']['Item'][k] = {'S': v}
                else:
                    d['PutRequest']['Item'][k] = {'N': v}

            new_json['watches'].append(d)

        lines = [
            'aws dynamodb create-table --cli-input-json file://../db/create-table-watches.json --region eu-west-3\n']

        batch_size = int(len(new_json['watches'])/25)+1
        
        for i in range(batch_size):
            with open(f'./db/adapted_watches_{i}.json', 'w') as outfile:
                json.dump(
                    {'watches': new_json['watches'][i*25:(i+1)*25]}, outfile, indent=4)
            lines.append(
                f'aws dynamodb batch-write-item --request-items file://../db/adapted_watches_{i}.json\n')

        with open(f'./info-v2/initialize_dynamodb.sh', 'w') as outfile:
            outfile.writelines(lines)
