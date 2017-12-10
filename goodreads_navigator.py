from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")


def setup_browser(is_headless):
    """
    This method setups the Chrome based Selenium browser that logs into Goodreads using the login information stored in
    the settings file.

    :param is_headless: A boolean value that indicates whether the browser is headless or not i.e. does the browser
    display graphically.
    :return: The browser that the method creates after it attempts to login.
    """

    # Setup your browser object and its options.
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'credentials_enable_service': False})
    # The parameter value determines whether or not the browser is visually shown.
    if is_headless:
        options.add_argument("headless")
    browser = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)

    # Setup the username and password from the config file.
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
    """
    This method returns a list of all valid genres on Goodreads.

    :return: A list of string containing the genres.
    """
    genres = "Art, Biography, Business, Chick-lit, Children's, Christian, Classics, Comics, Contemporary, Cookbooks, " \
             "Crime, Ebooks, Fantasy, Fiction, Gay and Lesbian, Graphic novels, Historical fiction, History, Horror, " \
             "Humor and Comedy, Manga, Memoir, Music, Mystery, Non-fiction, Paranormal, Philosophy, Poetry, " \
             "Psychology, Religion, Romance, Science, Science fiction, Self help, Spirituality, Sports, Suspense, " \
             "Thriller, Travel, Young-adult".replace(", ", "!").replace(" ", "%20").split("!")
    return genres


def get_genres_to_parse():
    """
    This method calculates which genres' giveaways to enter based on user set ignore preferences.

    :return: A list of URL to genre pages whoses giveaways are to be entered.
    """

    # Open the ignore settings file for reading.
    ignore_settings = open("ignore.txt", "r")
    # Get a list of all avaiable genres in Goodreads.
    all_genres = get_genre_list()
    # Create a list to store the URL for each of the valid genres.
    genres_to_parse = []

    # Go through every line in the ignore settings file and remove them from the genres list if they are in the file.
    for line in ignore_settings:
        line = str(line).replace("\n", "")
        if line in all_genres:
            all_genres.remove(line)

    # Go through every valid genre and create the URL from them. Return the list after that.
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
    """
    This method takes a passed in giveaway URL and enters said giveaway.

    :param browser: The browser to use to navigate.
    :param giveaway_url_list: The URL address of the giveaway.
    """
    for giveaway in giveaway_url_list:
        try:
            # Navigate to the correct URL.
            browser.get(giveaway)

            # Select the first cached address on the user's account.
            browser.find_element_by_id("addressSelect3262933").click()

            browser.find_element_by_name("want_to_read").click()
            # Click the button that agrees to the terms of entry.
            browser.find_element_by_name("entry_terms").click()
            # Click the submit button to enter the giveaway.
            browser.find_element_by_name("commit").click()
        except(NoSuchElementException):
            continue

def main():
    browser = setup_browser(False)
    all_urls = []
    for genre in get_genres_to_parse():
        all_urls.extend(get_all_href_list_genre(browser, genre))
        enter_giveaways(browser, all_urls)
        all_urls.clear()
    browser.close()


main()