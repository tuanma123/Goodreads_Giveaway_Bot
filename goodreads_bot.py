import goodreads_navigator as navigator

browser = navigator.setup_browser(False)
for genre in navigator.get_genres_to_parse():
    genre_alone = genre.replace("https://www.goodreads.com/giveaway/genre/", "").replace("?all_countries=true", "")
    navigator.enter_giveaways(browser, navigator.get_all_giveaways_by_genre(browser, genre), genre_alone)
browser.close()