from selenium import webdriver
import configparser


def setup_browser(is_headless):
    # Setup your browser object and its options.
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'credentials_enable_service': False})
    # The parameter value determines whether or not the browser is visually shown.
    if is_headless:
        options.add_argument("headless")
    browser = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)

    # Setup a parser for the config
    config = configparser.ConfigParser()
    config.read("settings.ini")
    username = config["credentials"]["username"]
    password = config["credentials"]["password"]

    # Navigate to the Goodreads website and then
    browser.get("https://www.goodreads.com/user/sign_in?source=home")

    # Input the username field.
    username_location = browser.find_element_by_id("user_email")
    username_location.send_keys(username)

    # Input the password field.
    password_location = browser.find_element_by_id("user_password")
    password_location.send_keys(password)

    # Send the information.
    browser.find_element_by_tag_name("input").submit()

    return browser


def get_genre_list():
    genres = "Art, Biography, Business, Chick-lit, Children's, Christian, Classics, Comics, Contemporary, Cookbooks, " \
             "Crime, Ebooks, Fantasy, Fiction, Gay and Lesbian, Graphic novels, Historical fiction, History, Horror, " \
             "Humor and Comedy, Manga, Memoir, Music, Mystery, Non-fiction, Paranormal, Philosophy, Poetry, " \
             "Psychology, Religion, Romance, Science, Science fiction, Self help, Spirituality, Sports, Suspense, " \
             "Thriller, Travel, Young-adult".replace(", ", "!").replace(" ", "%20").split("!")
    return genres


def get_genres_to_parse():
    ignore_settings = open("ignore.txt", "r")
    all_genres = get_genre_list()
    genres_to_parse = []
    for line in ignore_settings:
        if line in all_genres:
            all_genres.remove(line)
    for genre in all_genres:
        genres_to_parse.append("https://www.goodreads.com/giveaway/genre/" + genre + "?all_countries=true")
    return genres_to_parse


def get_href_list_page(browser, page_link):
    browser.get(page_link)
    giveaway_url_list = []
    giveaway_list_elements = browser.find_elements_by_class_name("gr-button")
    for item in giveaway_list_elements:
        if item.get_attribute("href") is not None:
            giveaway_url_list.append(item.get_attribute("href"))
    return giveaway_url_list


def get_all_href_list_genre(browser, root_link):
    page_number = 1
    giveaway_url_list = []
    while True:
        url = root_link + "&page=" + str(page_number)
        giveaway_urls = get_href_list_page(browser, url)
        if len(giveaway_urls) == 0:
            break
        else:
            giveaway_url_list.extend(giveaway_urls)
        page_number += 1
    return giveaway_url_list


def enter_giveaways(browser, giveaway_url_list):
    for giveaway in giveaway_url_list:
        browser.get(giveaway)

        address = browser.find_element_by_id("addressSelect3262933").click()
        want_to_read = browser.find_element_by_name("want_to_read").click()
        entry_term = browser.find_element_by_name("entry_terms").click()
        submit = browser.find_element_by_name("commit").click()

def main():
    browser = setup_browser(False)
    all_urls = []
    for genre in get_genres_to_parse():
        all_urls.extend(get_all_href_list_genre(browser, genre))
    enter_giveaways(browser, all_urls)

main()


