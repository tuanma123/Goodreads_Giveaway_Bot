#! /usr/bin/env python
"""
This scripts provides an utility for users to easily create settings files for the main script to
use.
"""
import os
import goodreads_navigator as navigator

print("Welcome. This script helps you create a new user setting file. Escape using your system's "
      "escape sequence to close (ctrl + c for Linux).")
username = input("Please input a Goodreads account username.")
while os.path.exists(username + ".ini"):
    username = input("Username configuration already exists, please enter a new one.")
password = input("Please input the corresponding account password.")
country = input("Please input the code for your country (e.g. enter US for the United States).")
logging = input("Would you like the bot to create log files whilst parsing (y/n)?")
logging = logging == "y"
headless = input("Would you like the browser to graphically display whilst the bot "
                 "runs(y/n)?")
headless = headless == "y"
ignore_list = []
print("Printing a list of genres. Please enter any categories you wish to ignore. Enter \"quit\' to"
      "continue.")
for genre in navigator.get_genre_list():
    print(genre.replace("%20", " "))
ignore = ""
while not ignore.lower() == "quit":
    ignore = input()
    if ignore.replace(" ", "%20") not in navigator.get_genre_list():
        print("Invalid input. Ignoring.")
        continue
    ignore_list.append(ignore)

settings_file = open(username + ".ini", "w")
settings_file.write("[credentials]\n")
settings_file.write("username=" + username + "\n")
settings_file.write("password=" + password + "\n")
settings_file.write("country=" + country + "\n")
settings_file.write("[settings]\n")
settings_file.write("headless=" + str(headless).lower() + "\n")
settings_file.write("logging=" + str(logging).lower() + "\n")
settings_file.write("[ignore]\n")
for x in range(0, len(ignore_list)):
    settings_file.write(str(x) + "=" + ignore_list[x] + "\n")