# Goodreads Giveaway Bot
This project is a Python based program that uses Python to allows user to enter giveaways from Goodreads.com 
programmatically using user specified settings. This projet was intended as a personal project for the purpose of my own
convenience and nothing more, others are free to use at their own risk.

The program uses a Selenium based web crawler to navigate to Goodreads's
giveaway pages and enter categories of giveaways based on user settings. All available giveaways are entered for every
valid genre of book. The program will log giveaways that have been successfully entered or that are unavailable to the 
user due to factors such as country restriction. If the program will ignore any giveaways that have already been entered
by the user.

## Requirements
* Python 3.X
* Selenium
* Google Chrome

##Usage
Note: This program has only been tested with Windows so far. Use without other operating systems at your own risk. 
Support for other operating systems will come at a later time.

The first thing that the user should do is fill in the user settings file located in settings.ini. This file provides
the user specified settings for the program to use. It is vital that that the user specify these values. An example
settings file will be provided with the program.

After initialising the values in the settings file, the user should call it from the command line using the following 
command:


Windows:
To use the parser install the required libraries with followings commands:
```shell
PATH_TO_PYTHON_INTERPRETER  goodsreads_bot.py
```
Replace the variables with the actual path of your Python interpreter and goodreads_bot.py. If you want to instead 
python.exe for the Python interpreter path you must add the Python interpreter to PATH environment variable.


Linux and Mac:
To use the parser install the required libraries with followings commands:
```shell
$ python goodreads_bot.py
```
Note that this is program has not be officially testesd on UNIX based systems such as Linux and Mac and may break in 
these cases due to the file traversal system being different.

### Settings
The following is what each line in the settings file indicates:

[credentials]<br></br>
username=Your Goodreads.com username<br></br>
password=Your Goodreads.com password<br></br>
country=The country code for your country of residence (US for the United States)<br></br>
[browsing]<br></br>
headless=This option determines whether the browser should be hidden or graphically displayed when it is crawling. 
Usually this should be set to true to indicate that it should not be displayed.<br></br>
[logging]<br></br>
logging=This option determines whether the program logs the results of its attempt to enter giveaways. Set the value to
true if you want logs and false if you do not. The logs will be located /logs i.e. it is based on the base 
directory of goodreads_bot.py<br></br>


## Future Features
Here are some features that I would to implement one day, however there is no promise that they will ever come:
* Multithreading the browsers to improve the speed of the program as a whole.
* Adding a GUI for the setup of the settings file. It might be confusing to people who are not familiar with it such as
myself, therefore a GUI might make it easier to use.
* Adding a GUI for the program as a whole.