# Current URL
BASE_URL = "https://www.angrymetalguy.com/"

# Delay between requests, avoids hammering the website with many requests
GLOBAL_DELAY = 0.25

# Rating system from the side bar
# Reviews might use numbers or words for scores
RATING_SYSTEM = {
    "Iconic": "5.0",
    "Excellent": "4.5",
    "Great": "4.0",
    "Very": "3.5",  # this is actually "Very Good", but dropping "Good" simplifies the regex
    "Good": "3.0",
    "Mixed": "2.5",
    "Disappointing": "2.0",
    "Bad": "1.5",
    "Embarrassing": "1.0",
    "Pathetic": "0.5",
}

# Used to mark reviews that couldn't be scored, likely due to parsing Exceptions
UNKNOWN_SCORE_VALUE = "unknown"

# Albums below this score won't be added to the rotation playlist
SCORE_CUTOFF = 4.0
