#! /usr/bin/env python
"""
This scripts provides an utility for users to easily create settings files for the main script to
use.
"""
import os

print("Welcome. This script helps you create a new user setting file. Escape using your system's "
      "escape sequence to close (ctrl + c for Linux).")
username = input("Please input a Goodreads account username.\n")
while os.path.exists(username + ".ini"):
    username = input("Username configuration already exists, please enter a new one.\n")
password = input("Please input the corresponding account password.\n")
country = input("Please input the code for your country (e.g. enter US for the United States).\n")
logging = input("Would you like the bot to create log files whilst parsing (y/n)?\n")
logging = logging == "y"
headless = input("Would you like the browser to graphically display whilst the bot "
                 "runs(y/n)?\n")
headless = headless == "y"


settings_file = open(username + ".ini", "w")
settings_file.write("[credentials]\n")
settings_file.write("username=" + username + "\n")
settings_file.write("password=" + password + "\n")
settings_file.write("country=" + country + "\n")
settings_file.write("[settings]\n")
settings_file.write("headless=" + str(headless).lower() + "\n")
settings_file.write("logging=" + str(logging).lower() + "\n")
settings_file.write("[ignore]\n")