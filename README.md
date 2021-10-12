# Public APIs List Crawler

---

**github-api-crawler** is a console based application which crawls a github repository to get the api data for each category
and store it in a database.


###### Problem Statement

---

Public APIs [github repo](https://github.com/public-apis/public-apis) is a collective list of free APIs for use in
software and web development.

On the landing page of the repo, there are some list of categories for e.g. Animals, Art & Design,
Business etc.
Each category has some API Details, e.g. for Animals:

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

The application should crawl each category and fetch the API Details and store them in a database.

- **Rate Limiting**  - All requests to the above hosts are limited to **10 requests/minute**.
- **Authentication** - Each request needs a Bearer Token for authentication. Each token has an expiration of 5 minutes
- **Get Token**      - GET https://public-apis-api.herokuapp.com/api/v1/auth/token
- **Get categories** - GET https://public-apis-api.herokuapp.com/api/v1/apis/categories?page=1
- **Get api data**   - GET https://public-apis-api.herokuapp.com/api/v1/apis/entry?page=1&category=Animals


**Complete detailed documentation can be found here 
[Postman documentation](https://documenter.getpostman.com/view/4796420/SzmZczsh?version=latest).**

**NOTE**: Do not use any other APIs or scraping method to get the data.


###### Points to achieve

---

- Code should follow concept of OOPS
- Support for handling authentication requirements & token expiration of server
- Support for pagination to get all data
- Develop work around for rate limited server
- Crawled all API entries for all categories and stored it in a database


###### Steps to run code

---

The application is built using:
- python 3.9.0
- docker (version: 20.10.8)
- docker-compose (version 1.29.2)

For local run, docker and docker-compose is a pre-requisite. Documentation for installation can be found 
[here](https://www.docker.com/get-started) 


Once you have docker and docker-compose installed you can cd into the directory(assuming you cloned this project on local),
you can run - `docker-compose up` to run the complete stack.

This command will run a mongo-db container, a mongo-express server(to visually see the data) and the application. 
You can check the logs to understand the flow of the application.

Once completed, you can check the data visually by visiting `localhost:8081` on which express is running,
which is a UI way to check mongodb data.


Refer to [Dockerfile](https://github.com/priyakdey/github-api-crawler/blob/master/Dockerfile) to understand how the image is created.
*The image is currently under my personal namespace(for obvious reasons), so in case you are building the image locally
and trying it out, do change namespace in docker-compose file as well. Later, I shall change the compose file to build from
the image from the file itself*


###### Steps to run code locally

---

You can run the services using docker-compose-local.yaml - `docker-compose up -f docker-compose-local.yaml`
which will run a mongo db database and a mongo-express server to check the data.
Once setup done, you can run the code using your fav ide.
