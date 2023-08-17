Each folder contains a pdf describing the assignment, and a README which explains how to run the code.

- Assignment1 implements a flask server which displays the environments varialbes of the system from which it runs. This server was containerized with Docker.
- Project1 implements an API in flask described by a swagger specification which is used to query a MySQL database containing data about watches. Docker-compose was used to orchestrate both containers.
- Project2 uses the API from Project1 as a microservice which was deployed on Google Cloud alongside another microservice that queried images of watches from AWS S3. Container orchestration was achieved with Kubernetes.
- Project3 uses the API from Project1 but replaces the MySQL database with AWS DynamoDB. The API was made serverless and deployed on AWS Lambda.
