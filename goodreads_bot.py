import goodreads_navigator as navigator
import goodreads_logger

browser = navigator.setup_browser(False)
all_urls = []
for genre in navigator.get_genres_to_parse():
    all_urls.extend(navigator.get_all_giveaways_by_genre(browser, genre))
    navigator.enter_giveaways(browser, all_urls)
    all_urls.clear()
    browser.close()