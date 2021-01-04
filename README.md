# Bot_that_attends_online_classes
This bot can join and leave your classes on time, as well as give replies to specific phrases using speech recognition library and using google's api which listens to desktop audio while it's present in the class. The bot so far works with a google classroom to google meet work flow where it gets the link to your classes from google classrooms and then uses that to join your google meet classes. The timetable.txt file contains the timetable depending upon which it searches for which class to join. 

Specific parts of the code will need to be edited in order to make the bot work such as, the username and password for the google account, the links for the classes and the number of classes you have per day along with the start and end times of those classes.

The libraries that need to be installed for this to work are selenium (webdriver api to open an instance for chrome and navigate the webpages), speech recognition and pyautogui.

NOTE: in order for the speech recognition api to work you must have PyAudio installed 
