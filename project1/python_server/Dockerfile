from debian
add . /server
workdir /server
run apt update && apt -f -y install python3 && apt -f -y install python3-pip && pip3 install -r requirements.txt
entrypoint flask run --host=0.0.0.0 --port=1080
expose 1080