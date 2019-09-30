from debian
run apt update && apt -f -y install python3 && apt -f -y install python3-pip && pip3 install flask
add . /flask
workdir /flask
run chmod +x server.py
entrypoint ["/flask/server.py"]
expose 5000