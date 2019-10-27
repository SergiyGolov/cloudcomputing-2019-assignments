from debian
add . /server
workdir /server
run apt update && apt -f -y install python3 && apt -f -y install python3-pip && pip3 install -r requirements.txt
run chmod +x run.sh
entrypoint ["/server/run.sh"]
expose 1080