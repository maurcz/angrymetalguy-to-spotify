PACKAGE_NAME:=angrymetalguy_to_spotify

ROOT_SCRIPTS:=./run.py
TARGETS:=$(ROOT_SCRIPTS) ./$(PACKAGE_NAME)
FILES:=$(TOP_LEVEL_SCRIPTS) $(shell find ./$(PACKAGE_NAME) -name '*.py')

.PHONY: check format lambda-deploy venv

.env:
	@echo "SPOTIFY_CLIENT_ID=" >> .env
	@echo "SPOTIFY_CLIENT_SECRET=" >> .env
	@echo "SPOTIFY_USERNAME=" >> .env
	@echo "SPOTIFY_REDIRECT_URI=" >> .env
	@echo "SPOTIFY_PLAYLIST_50_ID=" >> .env
	@echo "SPOTIFY_PLAYLIST_45_ID=" >> .env
	@echo "SPOTIFY_PLAYLIST_40_ID=" >> .env
	@echo "SPOTIFY_PLAYLIST_35_ID=" >> .env
	@echo "SPOTIFY_PLAYLIST_30_ID=" >> .env
	@echo "SPOTIFY_PLAYLIST_25_ID=" >> .env
	@echo "SPOTIFY_PLAYLIST_20_ID=" >> .env
	@echo "SPOTIFY_PLAYLIST_15_ID=" >> .env
	@echo "SPOTIFY_PLAYLIST_10_ID=" >> .env
	@echo "SPOTIFY_PLAYLIST_05_ID=" >> .env
	@echo "SPOTIFY_PLAYLIST_ROTATION_ID=" >> .env
	@echo "NUMBER_OF_PAGES=" >> .env
	@echo "SUPRESS_SCRAPING_ERRORS=" >> .env

check:
	flake8 $(TARGETS)
	isort $(TARGETS) --check
	black $(TARGETS) --check

format:
	black $(TARGETS)
	isort $(TARGETS)

# This is just an example of a lambda deploy from local.
# You have to export two vars to your local env:
# - LOCAL_CACHE_FILE = The name of the `.cache-*` file generated after you've authenticated once
# - LAMBDA_FUNCTION_NAME = The name of your lambda function
# This command assumes you have both `poetry` and `aws` available in your terminal.
lambda-deploy:
	rm -r -f .lambda/
	rm -f lambda.zip
	mkdir .lambda/
	cp run.py .lambda/
	cp ${LOCAL_CACHE_FILE} .lambda/${LOCAL_CACHE_FILE}
	cp -r angrymetalguy_to_spotify .lambda/angrymetalguy_to_spotify/
	poetry export -f requirements.txt --output .lambda/requirements.txt
	pip install -r .lambda/requirements.txt -t .lambda/
	cd .lambda; zip -r ../lambda.zip .
	aws lambda update-function-code --function-name ${LAMBDA_FUNCTION_NAME} --zip-file fileb://lambda.zip --no-cli-pager
	rm -f lambda.zip
	rm -r .lambda/

venv:
	virtualenv .venv --python=3.10
	. .venv/bin/activate; poetry install;