#!/usr/bin/env python
import goodreads_navigator as navigator
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

# Get the user specified setting that determines what kind of browser to use.
is_headless = config["browsing"]["headless"].lower()
if is_headless is "true":
    is_headless = True
else:
    is_headless = False

browser = navigator.setup_browser(is_headless)
for genre in navigator.get_genres_to_parse():
    genre_alone = genre.replace("https://www.goodreads.com/giveaway/genre/", "").replace("?all_countries=true", "")
    navigator.enter_giveaways(browser, navigator.get_all_giveaways_by_genre(browser, genre), genre_alone)
browser.close()