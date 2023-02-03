## Can we use a database? What for? SQL or NoSQL?
We can use a database:
- User authentication against the provided api
- Caching of results to reduce the requests against the gists.github.com API

NoSQL or Key-Value - for caching
SQL - can be used for authentication (holding user credential data)

# How can we protect the api from abusing it?
We can introduce request rate-limiting. There is a package flask-limiter that provides a decorator for our endpoints.
It will require however a backend like redis, memcached or MongoDB.

# How can we deploy the application in a cloud environment
We can deploy the application using the created docker-container on different Cloud platforms like AWS, GCP, Azure,
but this will require some additional configuration and container registry, where we can push our docker-container.

# How can we be sure the application is alive and works as expected when deployed into a cloud environment
- We could use the "/ping" route for a healthcheck
- We could implement metrics monitoring using prometheus/statsd

# Any other topics you may find interesting and/or important to cover
- Since no caching was implemented - I decided that pagination on the client side doesn't make sence.
- Handling the actual matching could've been done using asyncio instead of Theads, but that would be better with async
  client like aiohttp or httpx and perhaps with an async framework like fastapi/quart/startlette/tornado