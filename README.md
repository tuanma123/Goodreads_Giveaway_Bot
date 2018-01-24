# Goodreads Bot
This is a program that allows user to enter Goodreads.com giveaways without requiring any manual
user input. The program operates through user configuration files (ini files) to automatically log
in and crawl through all book giveaways, ignoring sections based on user configuration settings.

## Usage
The program operates through the main program located in goodreads_bot.py. To operate the program
simply run goodreads_bot.py using the appropriate method for the operating system. At runtime the
program will look for any configuration files in the current directory to build up the user
settings. The program will then operate based on the configuration files it found.

Note:
At this time, the program only supports Windows. The core program is not system bound, however the
Selenium driver is Windows specific. In order to support more OS platforms, the Selenium driver
needs to be updated for other operating systems. However, that is not yet officially supported yet.