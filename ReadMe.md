# Economic Inactivity Dashboard

This repository contains the dashboard which gives insights into economic inactivity over time. It is also hosted online through this [link](https://economic-inactivity-uk-2a720dbd86e4.herokuapp.com/)

## directory structure
- `.github/`: contains workflows for automated unit testing.
- `src/`: contains the python/html templates to create a Flask application
- `tests/`: contains unit tests to validate whether the outputs 


## running code
If you would like to run this code locally, follow the steps below:
- create a virtual environment by running `python -m venv venv`
- enter the environment (depending on what OS you have this may be different, Windows OS is `venv\Scripts\activate`).
- run `pip install -r requirement.txt` and subsequently `python3 -m pip install xlrd` to ensure you have the necessary packages in the correct version to replicate the project work.
- finally to run locally while also tests pass run `python -m src.main` (This ensures that Python recognizes the package structure correctly and also ensures the unit test passes).

**NOTE**: I recommend viewing the output in Microsoft Edge since the HTML templates designed by ONS seem to be optimised for Edge.
- once you are done exit the environment by `deactivate`

## running test
This code base has a 100% unit test coverage (except the main.py file). To run the unit tests use the command `pytest -vv -s --cov=src` which would provide a coverage report as well as an extensive log as to the potential passing/failing tests.

## future work
Currently, this is run locally, however, wouldn't it be nice to deploy this remotely so anyone can access it? There are numerous ways to go about this such as using one of the cloud providers or using a simpler solution such as Heroku?
