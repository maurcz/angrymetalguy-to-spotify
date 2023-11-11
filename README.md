# Angry Metal Guy to Spotify

This project periodically adds reviews from https://www.angrymetalguy.com/ to spotify playlists. The process runs once every Sunday morning (EST).

All playlists are public, created under my own username, and **can be accessed by anyone**.

## Rotation Playlist

Contains all albums with ratings 4.0 (Great) and up. Tracks that have been in the playlist for more than `60` days are removed:
- https://open.spotify.com/playlist/6aKz4X7BhEdKG7fsDqc4lA?si=fa3aca50eb6540f1


## Score Based

Reviews scraped by this project, categorized according to ratings:
- 5.0: https://open.spotify.com/playlist/1c6n4bDdWcZGHzecPrg0C4?si=ff31b54f72834dc3
- 4.5: https://open.spotify.com/playlist/4xkM9lzAoM6y8AGzHcWIv7?si=7e036dee8b4c4efb
- 4.0: https://open.spotify.com/playlist/5QTnjHEsZBh3PlNdndoa2C?si=e1a7c6a1cb4448af
- 3.5: https://open.spotify.com/playlist/1BI97XGwdXhh7nv1bekpZn?si=2b907d2555bb4f6f
- 3.0: https://open.spotify.com/playlist/0bclGj71DEVEzA5N3agmAP?si=86fbbb73941e4b08
- 2.5: https://open.spotify.com/playlist/4qu0nm6cSAuUg8hfYSGbJA?si=4258308744ae4538
- 2.0: https://open.spotify.com/playlist/7xEskoPIzzbgVYifBiVjOK?si=41be2a46ef2e4891
- 1.5: https://open.spotify.com/playlist/4R1FkZg2VIvggB7k8dfaQ7?si=bf3243f7cff44927
- 1.0: https://open.spotify.com/playlist/3tcK2Cu82wN3PaX3HBsF6d?si=eee906f67fea45a3
- 0.5: https://open.spotify.com/playlist/40idhH9MGKuyNLMHDHcbT3?si=755a432a83b14c49

Tracks that have been in the playlist for more than `365` days are removed.

## Limitations

Spotify might add, remove, or re-add albums to its catalog at any time. So if an album is missing from a playlist, this is the primary reason. The scraper is also not fail-proof; if a score can't be parsed, the album will simply be ignored. If there's any layout changes to the website, the scraper will have to be manually cleaned.

## Setup

Follow this section if you want to try running this project locally. Feel free to skip if all you care about are playlists!

Before we get into specifics, here's an overview of some of the tools that are used by this project:

- You'll need [poetry](https://python-poetry.org/) for dependency management.
- `make venv` to create a local environment.
    - This requires `poetry` for dep management. I recommend installing `poetry` using [pipx](https://www.youtube.com/watch?v=FyA4i_dP934).
    - If you don't use [virtualenv](https://virtualenv.pypa.io/en/latest/), create the python environment using whatever you like.
        - Note that you'll still have to run `poetry install` inside the enviroment.
- All credentials and configs are read from env vars. Use `make .env` to create a local `.env` file with the variables you need. Fill out with your own information / configs.

### Spotipy Setup

Anything spotify-related is done using a python package called [spotipy](https://github.com/spotipy-dev/spotipy). Since this is not a project with a UI, there's a slightly annoying process you'll have to go through when running for the first time:

- Go to https://developer.spotify.com/ and register a new app. Add the following to your local `.env`:
    - `SPOTIFY_CLIENT_ID`: app client id
    - `SPOTIFY_CLIENT_SECRET`: app client secret
    - `SPOTIFY_USERNAME`: your spotify username
    - `SPOTIFY_REDIRECT_URI`: a redirect URL for the auth process. Since this is backend, I recommend something simple like http://localhost/8081/

When you do `python run.py` for the first time, spotipy will give you a link in your terminal. Click on that link, authenticate to Spotify in your browser and paste the redirect link back into your terminal (the link should start with the dummy `SPOTIFY_REDIRECT_URI` you've used, i.e. http://localhost/8081). This will create a local `.cache-<spotify-username>` file in the app directory (the file is .gitignored).

Now all is left is to find your target playlist ids. To do this:
- Right-Click the playlist in spotify and choose _Share_ -> _Copy link to playlist_.
- The part after `/playlist/` and before `?` is the playlist id. So for https://open.spotify.com/playlist/52a8LeWcFcYtHhGMHJooHN?si=9c4eea62db564db7, the id is `52a8LeWcFcYtHhGMHJooHN`.

You obviously won't be able to add other user's playlists, unless you're a collaborator to that playlist.

### Configuration

You can change the behavior of this app by changing the following inside `.env`:

- `SCORE_CUTOFF`: Only scores equal or above this number will be added to the rotation playlist. AMG reviews go from 0.5 to 5.0 - the value should be a float.
- `NUMBER_OF_PAGES`: Number of pages to scrape each time. I leave this at 4 for weekly runs, but you go as far as you want. There's a global constant that adds a small delay between page hits, so that this project won't overwhelm their server(s).
- `SUPRESS_SCRAPING_ERRORS`: Only relevant if deploying to lambdas (if fails _even_ if all you're doing is logging an exception). Leave as `False` for local runs.

## Deployment

I use a combo of AWS Lambda and Amazon EventBrige to run this app on a schedule. To simplify the deployment process, I've added a `make lambda-deploy` command that creates a `zip` file with the code and all dependencies, then uploads to your lambda using the [aws](https://aws.amazon.com/cli/) cli.

Add the values you have in your local `.env` file as Environment Variables in the lambda configuration.

Note that you **must** have a local `.cache-*` file created before uploading this to lambda, otherwise spotipy _won't_ work. I'd rather have this as an env var or something, but couldn't find any alternatives. It's a compromise, but this file only holds a temporary key that expires very quickly, refreshing every new time you try to access by using your ClientID + ClientSecret. The scope of the access is also decreased as much as possible (can only modify playlists and nothing else).

EventBridge should be easy to configure once you have your lambda up. Just go to _Schedules_ and add a new Cron Expression, using your lambda as the target.
