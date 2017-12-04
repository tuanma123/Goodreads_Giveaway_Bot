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
    send_button = browser.find_element_by_tag_name("input").submit()

    return browser


def get_genre_list():
    genres = "Art, Biography, Business, Chick-lit, Children's, Christian, Classics, Comics, Contemporary, Cookbooks, " \
             "Crime, Ebooks, Fantasy, Fiction, Gay and Lesbian, Graphic novels, Historical fiction, History, Horror, " \
             "Humor and Comedy, Manga, Memoir, Music, Mystery, Non-fiction, Paranormal, Philosophy, Poetry, " \
             "Psychology, Religion, Romance, Science, Science fiction, Self help, Spirituality, Sports, Suspense, " \
             "Thriller, Travel, Young-adult".replace(", ", "!").replace(" ", "%20").split("!")
    return genres

def parse_genre(genre, browser):
    browser.get("https://www.goodreads.com/giveaway/genre/" + genre)
    print(browser.page_source)
browser = setup_browser(False)
parse_genre("Art", browser)
