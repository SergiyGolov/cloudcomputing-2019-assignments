# Cloud Computing Project 2 - Watches Webservices

Goloviatinski Sergiy
Herbelin Ludovic

## State of the project

Everything is working as expected, up to the end of the project with the deployment in the `all.yaml` file and the rolling upgrade.


## Testing

Endpoints :
- 35.244.196.84/info/v1/
- 35.244.196.84/image/v1/


You can use the following URLs to check the services :

- **Info service** : http://35.244.196.84/info/v1/watch/complete-sku/A
    - You will be prompted to login, type the following values
        - **Username** : `cloud`
        - **Password** : `computing`
    - This path will return a list of watches with SKUs starting with 'A'
- **Image service** : http://35.244.196.84/image/v1/watch/CAC1111.BA0850
    - This path will show a very cool TAG HEUER watch image


Or using the commands : 
- **Info service** : `curl -X GET "http://35.244.196.84/info/v1/watch/complete-sku/A" -H "accept: 'application/json" -H "Authorization: Basic Y2xvdWQ6Y29tcHV0aW5n"`
- **Image service** : `curl -X GET "http://35.244.196.84/image/v1/watch/CAC1111.BA0850" --output watch.png` (will output the image to the 'watch.png' file)


## Miscellaneous informations

### Google Cloud Kubernetes Cluster

We had to increase the cluster's number of nodes to 3, since when we added the Google CloudSQL Proxy, we started getting an error "Cannot schedule pods. Insufficient CPU.". Increasing it fixed the error.


### Flask server

We had to add routes on '/' for both services to allow the ingress to perform the healthcheck. Those return a basic message, with the HTTP code 200.

We had concurrency issues with the MYSQL DB connector, because of concurrent accesses. 
The solution we found was to recreate it for every request, which might not be the best way but since the goal of this project is to deploy and work with Kubernetes, we think it is sufficient.