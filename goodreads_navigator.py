"""
Note that this file provides the functionality for navigating to pages on Goodreads and scrapping
the pages for valid giveaway links. The navigator will navigate to pages based on user specified
settings, scrap the valid giveaways and then log giveaways entered. A giveaway is valid if and only
if the user has not yet entered the giveaway and is in a genre that the user desires to enter.
"""


import selenium.common.exceptions as exceptions
from selenium import webdriver
import datetime
import time
import os
import configparser


def setup_user_settings():
    """
    This method crawls through the current directory and makes a list of maps, where each contains
    the user specified information from the ini files.

    :return: A list of maps containing the user settings from every ini file.
    """
    ini_list = []
    config = configparser.ConfigParser()
    for file in os.listdir(os.getcwd()):
        if file.endswith(".ini"):
            config.read(file)
            username = config["credentials"]["username"]
            password = config["credentials"]["password"]
            country = config["credentials"]["country"]
            logging = config["settings"]["logging"].lower() == "true"
            headless = config["settings"]["headless"].lower() == "true"
            ignore_list = []
            for item in config["ignore"]:
                ignore_list.append(config["ignore"][item])
            user_map = {"username":username, "password":password, "country":country,
                        "logging": logging, "headless":headless, "ignore":ignore_list}
            ini_list.append(user_map)
    return ini_list


def setup_entries_map(username):
    """
    This creates a map of genres to giveaways that have been previously entered in that genre.
    Crawls through the existing log files and then populates the maps with the corresponding
    information.

    :param username: The current user.
    :return: A map containing all the previously entered giveaways for the user.
    """
    if not os.path.exists("logs"):
        os.makedirs("logs")
    entries_map = {}
    if not os.path.exists("logs/" + username):
        os.makedirs("logs/" + username)
    if not os.path.exists("logs/" + username + "/successful"):
        os.makedirs("logs/" + username + "/successful")
    if not os.path.exists("logs/" + username + "/failure"):
        os.makedirs("logs/" + username + "/failure")
    for log_folder in os.listdir("logs/" + username):
        for log_file in os.listdir("logs/" + username + "/" + log_folder):
            for line in open("logs/" + username + "/" + log_folder + "/" + log_file):
                line = line.replace("\n", "")
                giveaway = line[:line.find(",")]
                genre = log_file[:-4]
                if genre in entries_map:
                    entries_map[genre].append(giveaway)
                else:
                    entries_map[genre] = []
    return entries_map


def setup_browser(is_headless, username, password):
    """
    This method setups the Chrome based Selenium browser that logs into Goodreads using the login information stored in
    the settings file.

    :param is_headless: A boolean value that indicates whether the browser is headless or not i.e. does the browser
    display graphically.
    :param username: The Goodreads username of the current user.
    :param password: The Goodreads password of the current user.
    :return: The browser that the method creates after it attempts to login.
    """

    # Setup your browser object and its options.
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'credentials_enable_service': False})
    # The parameter value determines whether or not the browser is visually shown.
    if is_headless:
        options.add_argument("headless")
    browser = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)

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
    genres = "Art, Biography, Business, Chick-lit, Children's, Christian, Classics, Comics, " \
             "Contemporary, Cookbooks, Crime, Ebooks, Fantasy, Fiction, Gay and Lesbian, Graphic " \
             "novels, Historical fiction, History, Horror, Humor and Comedy, Manga, Memoir, " \
             "Music, Mystery, Non-fiction, Paranormal, Philosophy, Poetry, Psychology, Religion, " \
             "Romance, Science, Science fiction, Self help, Spirituality, Sports, Suspense, " \
             "Thriller, Travel, Young-adult".replace(", ", "!").replace(" ", "%20").split("!")
    return genres


def get_genres_to_parse(ignore_list):
    """
    This method calculates which genres' giveaways to enter based on user set ignore preferences.

    :return: A list of URL to genre pages whose giveaways are to be entered.
    """
    # Get a list of all avaiable genres in Goodreads.
    all_genres = get_genre_list()
    # Create a list to store the URL for each of the valid genres.
    genres_to_parse = []

    # Remove all genres in the ignore list.
    for ignore in ignore_list:
        all_genres.remove(ignore.replace(" ", "%20"))

    # Go through every valid genre and create the URL from them. Return the list after that.
    for genre in all_genres:
        genres_to_parse.append("https://www.goodreads.com/giveaway/genre/" + genre +
                               "?all_countries=true")
    return genres_to_parse


def get_giveaway_links(browser, page_link):
    """
    Navigates to a page using the given URL using the browser and then parses through all the
    buttons on the page for the the link te the assigned giveaway and returns all the valid URLs as
    a list.

    :param browser: The browser to use to navigate.
    :param page_link: A URL link to the page containing the giveaway buttons.
    :return: A list containing the URLs of all the giveaways on the passed page.
    """
    # Navigate to the passed page.
    browser.get(str(page_link))
    giveaway_url_list = []

    # Find all the references to the buttons(in this case they are gr-buttons.
    giveaway_list_elements = browser.find_elements_by_class_name("gr-button")

    # Go through every every button and add their href to the list if the href is not empty.
    for item in giveaway_list_elements:
        if item.get_attribute("href") is not None:
            giveaway_url_list.append(item.get_attribute("href"))

    return giveaway_url_list


def enter_giveaways(browser, giveaway_url_list, genre, username, user_country, logging):
    """

    :param browser:
    :param giveaway_url_list:
    :param genre:
    :param username:
    :param user_country:
    :param logging:
    :return:
    """
    # Open the log files for the genre.
    success_log = open("logs/" + username + "/successful/" + genre + ".csv", "a")
    failure_log = open("logs/" + username + "/failure/" + genre + ".csv", "a")
    previous_entries = setup_entries_map(username)

    for giveaway in giveaway_url_list:
        # Try to navigate through all the appropriate buttons and click them. If anything turns out
        # to missing, just skip the giveaway.
        if giveaway in previous_entries:
            continue
        try:
            # Navigate to the correct URL.
            browser.get(str(giveaway))

            # Get the list of valid countries and format it appropriately by deleting all the extra
            # text and weird characters. Check if the user's country is valid in the giveaway and
            # attempt to enter it if it is. Whatever outcomes occurs, log it in the repository.
            countries = browser.find_element_by_class_name("mainContentContainer").text. \
                split("\n")[3][66:].replace(".", "").replace(" and", ",").split(", ")
            if user_country in countries:
                # Select the first cached address on the user's account.
                browser.find_element_by_class_name("gr-button--small").click()
                browser.find_element_by_name("want_to_read").click()
                # Click the button that agrees to the terms of entry.
                browser.find_element_by_name("entry_terms").click()
                # Click the submit button to enter the giveaway.
                browser.find_element_by_name("commit").click()

                if logging:
                    # Everything worked so log the giveaway entered with a timestamp.
                    timestamp = datetime.datetime.fromtimestamp(time.time()).\
                        strftime('%m-%d-%Y %H:%M:%S')
                    success_log.write(giveaway + "," + str(timestamp) + "\n")
            else:
                if logging:
                    # The user is in a invalid log, log that with a stamp in failure logs.
                    timestamp = datetime.datetime.fromtimestamp(time.time()).\
                        strftime('%m-%d-%Y %H:%M:%S')
                    failure_log.write(giveaway + "," + str(timestamp) + "," + "INVALID_COUNTRY\n")
        except (exceptions.NoSuchElementException, exceptions.WebDriverException):
            pass
            if logging:
                # Some browsing error occurred, log that in failure logs with a timestamp.
                timestamp = datetime.datetime.fromtimestamp(time.time()).\
                    strftime('%m-%d-%Y %H:%M:%S')
                failure_log.write(giveaway + "," + str(timestamp) + "," + "BROWSER_ERROR\n")
            continue
    failure_log.close()
    success_log.close()
