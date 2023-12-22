start: start-venv install-dependencies
	@echo "Starting project"
	python ./model/app.py;

install-dependencies:
	@echo "Installing dependencies"
	pip install -r model/requirements.txt;


start-venv:
	@echo "Starting virtual environment"
	source model/venv/bin/activate;

start-api:
	@echo "Starting API"
	uvicorn main:app --reload --port 8000;


start-api-prod: install-depencecies-prod
	@echo "Starting API"
	pm2 delete all;
	pm2 start "python -m uvicorn main:app --port 8000" --name "chess-api";

install-depencecies-prod:
	@echo "Installing dependencies"
	pip install -r requirements.txt;
