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


###### Steps to run/debug code locally

---

You can run the services using docker-compose-local.yaml - `docker-compose up -f docker-compose-local.yaml`
which will run a mongo db database and a mongo-express server to check the data.
Once setup done, you can run the code using your fav ide.


Also, change line [number 5](https://github.com/priyakdey/github-api-crawler/blob/master/crawler/constants.py#L5) to: 
`DB_CONN_STRING = "mongodb://admin:password@localhost:27017/"`

- Create and activate your virtual env
- Install the dependencies by running - `pip install -r requirements-dev.txt`

**NOTE** - Ignore the linux dev requirements file with lots of stuff which is specially needed for my wsl setup and vim
to work. So ignore that!

###### Improvements

---

Since this was a project asked for an interview review to a friend, I am not going to post the complete question,
but follow the instructions and add improvements which I think can be done given more time. (A weekend was given for this).

1. **Configuration Driven** - The database URLs will differ depending on different envs. 
One example is changing the URL in constants.py file when running on local and not as a stack, which I do not like.
So the URLs needs to be config driven. Open issue [#21](https://github.com/priyakdey/github-api-crawler/issues/21))
is there for this.
2. **Performance** - Though python is not a good multithreaded platform, I can leverage multiprocess and implement 
a Pub-Sub model to speed up the process; the producer pushed the data to a Pipe (I can use SQS maybe and in that case
switch to Dynamo or still use Mongo Service) while the consumer keeps pushing the data to the DB. This might not give a huge
performance benefit specially on local db, since currently after the data fetch, the collection.insert_many takes few ms
to load the complete data, but in real time with cloud services and geo-location, this might be an advantage.
3. **Design Patterns** - I need to revist the complete design and check for more python code and optimisation that can be done.

