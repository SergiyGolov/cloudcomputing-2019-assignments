#!/usr/bin/env bash
docker run -d -p 1080:1080 --network=host \
-e "FLASK_APP=server.py" \
-e "HTTP_USER=cloud" \
-e "HTTP_PASS=computing" \
-e "DB_HOST=127.0.0.1" \
-e "DB_PORT=3306" \
-e "DB_DBNAME=watches" \
-e "DB_USER=watches" \
-e "DB_PASS=watches" \
info-service-v2