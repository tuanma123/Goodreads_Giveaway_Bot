"""
Note that this file provides the functionality for navigating to pages on Goodreads and scrapping the pages for valid
giveaway links. The navigator will navigate to pages based on user specified settings, scrap the valid giveaways and
then log giveaways entered. A giveaway is valid if and only if the user has not yet entered the giveaway and is in a
genre that the user desires to enter.
"""


import selenium.common.exceptions as exceptions
from selenium import webdriver
import configparser
import datetime
import time
import os


def setup_log_list(log_path):
    log_list = []
    for log_file in os.listdir(log_path):
        for line in open(log_path + "/" + log_file):
            log_list.append(line)
    return log_list


config = configparser.ConfigParser()
config.read("settings.ini")
success_list = setup_log_list("logs/successful")
failure_list = setup_log_list("logs/failure")


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

    :return: A list of URL to genre pages whose giveaways are to be entered.
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


def get_giveaway_links(browser, page_link):
    """
    Navigates to a page using the given URL using the browser and then parses through all the buttons on the page for
    the the link te the assigned giveaway and returns all the valid URLs as a list.

    :param browser: The browser to use to navigate.
    :param page_link: A URL link to the page containing the giveaway buttons.
    :return: A list containing the URLs of all the giveaways on the passed page.
    """
    # Navigate to the passed page.
    print(page_link)
    browser.get(str(page_link))
    giveaway_url_list = []

    # Find all the references to the buttons(in this case they are gr-buttons.
    giveaway_list_elements = browser.find_elements_by_class_name("gr-button")

    # Go through every every button and add their href to the list if the href is not empty.
    for item in giveaway_list_elements:
        if item.get_attribute("href") is not None:
            giveaway_url_list.append(item.get_attribute("href"))

    return giveaway_url_list


def get_all_giveaways_by_genre(browser, root_link):
    """
    For a given genre, this page will try to navigate every possible page number for that specific genre until it
    reaches a page that does not contain any more giveaway links. Returns all valid giveaway links for that genre.

    E.g. for genre = "Art" it will navigate to the 1st
    art page, the 2nd page, and so on until there are no more pages.

    :param browser:
    :param root_link:
    :return:
    """

    # Start at 1 and navigate to every page, incrementing page number until you reach a page that no longer contains
    # buttons for giveaways.
    page_number = 1
    giveaway_url_list = []
    while True:
        # Navigate to the correct page using the page number.
        url = root_link + "&page=" + str(page_number)
        # Attempt to get the giveaways URLs and if there are no URLs that means you have reached the end. Else you keep
        # adding it to the result list.
        giveaway_urls = get_giveaway_links(browser, url)
        if len(giveaway_urls) == 0:
            break
        else:
            giveaway_url_list.extend(giveaway_urls)
        page_number += 1

    return giveaway_url_list


def enter_giveaways(browser, giveaway_url_list, genre):
    """
    This method takes a passed in giveaway URL and enters said giveaway.

    :param browser: The browser to use to navigate.
    :param giveaway_url_list: The URL address of the giveaway.
    """
    # Open the log files for the genre.
    success_log = open("logs/successful/" + genre + ".csv", "w")
    failure_log = open("logs/failure/" + genre + ".csv", "w")

    for giveaway in giveaway_url_list:
        # Try to navigate through all the appropriate buttons and click them. If anything turns out to missing,
        # just skip the giveaway.
        try:
            # Navigate to the correct URL.
            browser.get(str(giveaway))

            # Get the list of valid countries and format it appropriately by deleting all the extra text and weird
            # characters. Check if the user's country is valid in the giveaway and attempt to enter it if it is.
            # Whatever outcomes occurs, log it in the repository.
            user_country = config["credentials"]["country"]
            countries = browser.find_element_by_class_name("mainContentContainer").text.split("\n")[3][66:].\
                replace(".", "").replace(" and", ",").split(", ")
            if user_country in countries:
                # Select the first cached address on the user's account.
                browser.find_element_by_id("addressSelect3262933").click()

                browser.find_element_by_name("want_to_read").click()
                # Click the button that agrees to the terms of entry.
                browser.find_element_by_name("entry_terms").click()
                # Click the submit button to enter the giveaway.
                browser.find_element_by_name("commit").click()

                # Everything worked so log the giveaway entered with a timestamp.
                timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%m-%d-%Y %H:%M:%S')
                success_log.write(giveaway + "," + str(timestamp) + "\n")
            else:
                # The user is in a invalid log, log that with a stamp in failure logs.
                timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%m-%d-%Y %H:%M:%S')
                failure_log.write(giveaway + "," + str(timestamp) + "," + "INVALID_COUNTRY\n")
        except (exceptions.NoSuchElementException, exceptions.WebDriverException):
            # Some browsing error occurred, log that in failure logs with a timestamp.
            timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%m-%d-%Y %H:%M:%S')
            failure_log.write(giveaway + "," + str(timestamp) + "," + "BROWSER_ERROR\n")
            continue
    failure_log.close()
    success_log.close()
