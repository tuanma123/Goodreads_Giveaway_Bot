"""
This file acts as the main script for this Goodreads bot. Run this file to run the program for
every user that has a settings file.
"""
import goodreads_navigator as navigator

# Get the user settings for every user and then run the program for every user.
user_settings = navigator.setup_user_settings()
for user in user_settings:
    # Get all the user parameters from the map.
    username = user["username"]
    password = user["password"]
    country = user["country"]
    logging = user["logging"]
    print(logging)
    headless = user["headless"]
    ignore_list = user["ignore"]

    # Setup the browser for the user and then navigate through their desired giveaways and enter
    # them accordingly.
    browser = navigator.setup_browser(headless, username, password)
    for genre in navigator.get_genres_to_parse(ignore_list):
        genre_alone = genre.replace("https://www.goodreads.com/giveaway/genre/", "").replace(
            "?all_countries=true", "")
        navigator.enter_giveaways(browser, navigator.get_giveaway_links(browser, genre),
                                  genre_alone, username, country, logging)
    browser.close()