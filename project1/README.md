# Cloud computing, project 1, Sergiy Goloviatinski

- Everything works, the server respects the API specifications
    - use `run.sh` script in python_server directory to test the server on the local machine
    - use `build_container.sh` and then `run_container.sh` in python_server directory to test the server in a container
    - use `docker-compose up` in the project1 root directory to test the server and mysql containers together
- I've implemented the bonuses (index in db on sku + http expiration headers)
- A `FLASK_APP=server.py` env var has been added to the scripts, needed for the `flask run` command
- You have to use the `http://127.0.0.1:1080/info/v1` path to communicate with the server + http basic auth (username: **cloud** password: **computing**)
- You can test the API with the swagger editor, I've added the required CORS headers on the server side
- If you have any questions, email me at sergiy.goloviatinski@unine.ch