.PHONY: help

CMD:=poetry run
PYMODULE:=j5
TESTS:=tests
PROJECT:=gistapi


help:
	$(info Available targets:)
	$(info | help 		Show help message)
	$(info | checks		Run black and pylint to check code quality)
	$(info | test		Run pytest on project)
	$(info | test-cov 	Run pytest with coverage will generate htmlcov directory)
	$(info | run		Start local flask server)
	$(info | run-docker Start docker-container with docker-compose)
	$(info | clean 		Remove .pytest_cache and *.pyc files from project)

checks:
	$(CMD) black $(PROJECT) && $(CMD) pylint $(PROJECT) --max-line-length=120

test:
	$(CMD) pytest -vvv $(TESTS)

test-cov:
	$(CMD) pytest -cov=gistapi $(TESTS)

run:
	$(CMD) python run.py

run-docker:
	docker-compose up --build

clean:
	find . \( -iname "__pycache__" -o -iname ".hypothesis" \) -print0 | xargs -0 rm -rf
	-rm -rf .eggs *.egg-info/ .coverage build/ .cache .pytest_cache

%:
	echo "Target not found!"
	make help