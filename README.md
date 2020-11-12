# Test Suite for JokeGenerator
This is a set of automated tests for testing the JokeGenerator.

## Prerequisites

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pytest.

```bash
pip install -U pytest
```

## Run Tests
Copy the *Test* folder under joke-generator-master/JokeGenerator/. Under 
joke-generator-master/JokeGenerator/test, run

```bash
pytest test_JokeGenerator.py

# or

python test_JokeGenerator.py 

# Run only positive tests
pytest test_JokeGenerator.py -m positive
 
# Run only negative tests
pytest test_JokeGenerator.py -m negative
```

## View Results
See logs in test_JokeGenerator.log. Live logs will be displayed on the console during runtime.
An example log from a previous testrun is included (test_JokeGenerator.log.example).

## Limitation
- This automated test suite covers positive and negative functional tests for JokeGenerator.
- This automated test suite does not cover test cases handling error from the external APIs, eg. the external API server is down or the content of the response is corrupted. For this project, it is more feasible to cover those tests in unit tests with mocks.
