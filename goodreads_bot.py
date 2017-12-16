import goodreads_navigator as navigator

browser = navigator.setup_browser(False)
all_urls = []
for genre in navigator.get_genres_to_parse():
    genre_alone = genre.replace("https://www.goodreads.com/giveaway/genre/", "").replace("?all_countries=true", "")
    all_urls.extend(navigator.get_all_giveaways_by_genre(browser, genre))
    navigator.enter_giveaways(browser, all_urls, genre_alone)
    all_urls.clear()
    browser.close()