#!/usr/bin/env bash
# export AWS_PROFILE="zappa"
# # commands with # are not necessary for final deployment probably
# #docker pull lambci/lambda:build-python3.7
# alias zappashell3='docker run -ti -e AWS_PROFILE=$AWS_PROFILE -v "$(pwd):/var/task" -v ~/.aws/:/root/.aws  --rm docker build -t zappa_cloud_computing .'
# alias zappashell3 >> ~/.bash_profile

# # used to generate the zappa settings
# #zappa init

# cd zappa_project
# zappashell3
# virtualenv venv
# source venv/bin/activate
# pip install -r requirements.txt 

# docker build -t zappa_cloud_computing

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
zappa deploy dev
