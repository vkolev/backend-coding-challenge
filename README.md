# Challenge

This challenge is divided between the main task and additional stretch goals. All of those stretch goals are optional, but we would love to see them implemented. It is expected that you should be able to finish the challenge in about 1.5 hours. If you feel you are not able to implement everything on time, please, try instead describing how you would solve the points you didn't finish.

And also, please do not hesitate to ask any questions. Good luck!

## gistapi

Gistapi is a simple HTTP API server implemented in Flask for searching a user's public Github Gists.
The existing code already implements most of the Flask boilerplate for you.
The main functionality is left for you to implement.
The goal is to implement an endpoint that searches a user's Gists with a regular expression.
For example, I'd like to know all Gists for user `justdionysus` that contain the pattern `import requests`.
The code in `gistapi.py` contains some comments to help you find your way.

To complete the challenge, you'll have to write some HTTP queries from `Gistapi` to the Github API to pull down each Gist for the target user.
Please don't use a github API client (i.e. using a basic HTTP library like requests or aiohttp or urllib3 is fine but not PyGithub or similar).


## Stretch goals

* Implement a few tests (using a testing framework of your choice)
* In all places where it makes sense, implement data validation, error handling, pagination
* Migrate from `requirements.txt` to `pyproject.toml` (e.g. using [poetry](https://python-poetry.org/))
* Implement a simple Dockerfile
* Implement handling of huge gists
* Set up the necessary tools to ensure code quality (feel free to pick up a set of tools you personally prefer)
* Document how to start the application, how to build the docker image, how to run tests, and (optionally) how to run code quality checkers
* Prepare a TODO.md file describing possible further improvements to the archtiecture:
    - Can we use a database? What for? SQL or NoSQL?
    - How can we protect the api from abusing it?
    - How can we deploy the application in a cloud environment?
    - How can we be sure the application is alive and works as expected when deployed into a cloud environment?
    - Any other topics you may find interesting and/or important to cover


# Documentation

## Setting up development environment

Clone the repository:
```shell
git clone git@github.com/vkolev/backend-coding-challenge
```

Make sure you have poetry installed so running the following command will generate virtual environment for the project
automatically (providing the flag `--with dev` will ensure that the development dependencies are installed)

```shell
poetry intall --with dev
```

## Running Tests

To run the tests:

```shell
poetry run -v pytest
```

Or using the Makefile:
```shell
make test
```

## Code Quality

For code quality we use black and pylint 
- Black - to ensure consistent formatting
- pylint - to check for linting errors (we run it with --max-line-length=120 since 80 characters is too small for modern monitors)
- 
```shell
poetry run black gitstapi
poetry run pylint gistapi --max-line-length=120
```

Or using make:

```shell
make checks
```

## Runing the application

### Running the application with Flask Build-in server

```shell
poetry run python run.py
```

### Running the application with docker

```shell
docker-compose up --build
```