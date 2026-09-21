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
	@echo "LOCAL_CACHE_FILE=" >> .env
	@echo "LAMBDA_FUNCTION_NAME=" >> .env

check:
	uv run ruff check $(TARGETS)
	uv run ruff format $(TARGETS) --check

format:
	uv run ruff format $(TARGETS)
	uv run ruff check $(TARGETS) --fix

# This is just an example of a lambda deploy from local.
# Reads LOCAL_CACHE_FILE and LAMBDA_FUNCTION_NAME from your `.env` (or shell env).
# This command assumes you have both `uv` and `aws` available in your terminal.
lambda-deploy:
	@test -f .env || { echo "Missing .env - run 'make .env' first"; exit 1; }
	@set -e; \
	eval "$$(grep -E '^(LOCAL_CACHE_FILE|LAMBDA_FUNCTION_NAME)=' .env)"; \
	test -n "$$LOCAL_CACHE_FILE" || { echo "LOCAL_CACHE_FILE not set in .env"; exit 1; }; \
	test -n "$$LAMBDA_FUNCTION_NAME" || { echo "LAMBDA_FUNCTION_NAME not set in .env"; exit 1; }; \
	rm -r -f .lambda/; \
	rm -f lambda.zip; \
	mkdir .lambda/; \
	cp run.py .lambda/; \
	cp $$LOCAL_CACHE_FILE .lambda/$$LOCAL_CACHE_FILE; \
	cp -r angrymetalguy_to_spotify .lambda/angrymetalguy_to_spotify/; \
	uv export --no-dev --no-emit-project --output-file .lambda/requirements.txt; \
	pip install -r .lambda/requirements.txt -t .lambda/; \
	cd .lambda && zip -r ../lambda.zip . -x '*__pycache__*' -x '*.pyc'; \
	cd ..; \
	aws lambda update-function-code --function-name $$LAMBDA_FUNCTION_NAME --zip-file fileb://lambda.zip --no-cli-pager; \
	rm -f lambda.zip; \
	rm -r -f .lambda/

venv:
	uv sync --extra dev