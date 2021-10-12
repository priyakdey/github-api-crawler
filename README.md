# Public APIs List Crawler

---

Public APIs [github repo](https://github.com/public-apis/public-apis) is a collective list of free APIs for use in
software and web development.
Github API Crawler is an console-based application, which crawls the repository to get some data
and store it in a database.



###### Problem Statement

---

On the landing page of the above repo, there are some list of categories for e.g. Animals, Art & Design,
Business etc.
Each category has some API Details, e.g. for Animals, :

```json
{
  "API": "Cat Facts",
  "Link": "https://alexwohlbruck.github.io/cat-facts/",
  "Description": "Daily cat facts", 
  "Auth": "No", 
  "HTTPS": "Yes",
  "CORS": "No"
}
```


Tha application crawls the above list of API Details and stores it in a database.
**More detailed documentation can be found here 
[Postman documentation](https://documenter.getpostman.com/view/4796420/SzmZczsh?version=latest).**


###### Steps to run code

---

The application is built using:
- python 3.9.0
- docker (version: 20.10.8)
- docker-compose (version 1.29.2)

You can refer the [Dockerfile](https://github.com/priyakdey/github-api-crawler/blob/master/Dockerfile)
to check how the image is build.

[docker-compose file](https://github.com/priyakdey/github-api-crawler/blob/master/docker-compose.yaml) is used to
run mongo db, mongo express and the application as stack service.

For running the application locally, make sure to have docker-compose installed on your local machine
(version given above). Once done, travel to the directory the compose file is and then run the below command:
```shell
docker-compose up
```

This is going to run 3 services which includes the application itself. You can check the stack logs to see
the ongoing process.

Once completed, you can check the data visually by visiting `localhost:8081` on which express is running,
which is a UI way to check mongodb data.
