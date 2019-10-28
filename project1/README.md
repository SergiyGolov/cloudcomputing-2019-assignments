# Cloud computing, project 1, Sergiy Goloviatinski

Everything works, the server respects the API specifications
- use `run.sh` script in python_server directory to test the server on the local machine
- use `build_container.sh` and then `run_container.sh` in python_server directory to test the server in a container
- use `docker-compose up` in the project1 root directory to test the server and mysql containers together

The first time that you use `docker-compose up`, you will get the following error from the flask server: 
```
pymysql.err.OperationalError: (2003, "Can't connect to MySQL server on 'db' ([Errno 111] Connection refused)")
```
it's because the db isn't initialized yet, the flask server will automatically restart until the db is initialized (about 10-20 seconds), and then everything works as intended, the next time you will use `docker-compose up` the db will be already initialized and you won't get this error because I use a volume for the mysql container.

I've implemented the bonuses (index in db on sku + http expiration headers)

A `FLASK_APP=server.py` env var has been added to the scripts, needed for the `flask run` command

You have to use the `http://localhost:1080/info/v1` path to communicate with the server + http basic auth (username: **cloud** password: **computing**)

You can test the API with the swagger editor, I've added the required CORS headers on the server side

If you have any questions, email me at sergiy.goloviatinski@unine.ch