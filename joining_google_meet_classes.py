from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
import speech_recognition as sr
import os
from twilio.rest import Client #this is whatsapp web api which I used to ping me on whatsapp whenever the bot joins the class, beware that this requires a paid subscription
def joinGoogleClass():
    driver = webdriver.Chrome("E:/coding projects/chromedriver.exe")
    driver.set_window_position(0,0)
    driver.set_window_size(800, 800)
    driver.get("https://www.gmail.com")
    sleep(1)
    element = driver.find_element_by_name("identifier")
    element.send_keys("YourGmailID")
    element.send_keys(Keys.RETURN) 
    sleep(1)    
    element = driver.find_element_by_name("password")
    element.send_keys("YourGooglePassword")
    element.send_keys(Keys.RETURN)
    sleep(2)
    driver.get("https://www.classroom.google.com")
    print(driver.title)

def detectAudio(): #function that is called to convert audio into text
    r = sr.Recognizer()
    mic = sr.Microphone(device_index = 2)
    result = ""
    try:
        with mic as source:
            audio = r.listen(source , timeout=5 , phrase_time_limit= 15 )
        print("Analyzing for the text")
        result = r.recognize_google(audio)
        print(result)
    except:
        print("Its all good speak something into the mic")
    return result

def getTimeTable():
    file = open(r"C:\Users\TANAY GARG\AppData\Local\Programs\Python\Python38-32\timetable.txt") #edit this to the path to the timetable.txt file in your system
    text = file.read()
    text = text + "\n"
    list1 = []
    last_change_line = -1
    
    for i in range(0 ,len(text)):
        if(text[i] == '\n'):
            substring = text[last_change_line +1 : i]
            
            last_change_line = i
            if( not substring.isnumeric()):
                list1.append(substring)
    return list1

def dayToday():
    now =  datetime.now()
    day = now.strftime("%A")
    return day

def getTimeNow():
    now = datetime.now()
    hours = int(now.strftime("%H"))
    minutes = int(now.strftime("%M"))
    return hours, minutes

if __name__ == "__main__":
    timetable = getTimeTable() #gets the time table
    print(timetable)
    account_sid = "ACCount SID for twilio whatsapp api"
    auth_token = 'auth token for twilio whatsapp api' #edit these two only if you want a ping to your whatsapp number
    client = Client(account_sid, auth_token)
    firstClassTime = [8,0]
    #start and end times for the classes
    classTimings = [8, 9 , 10.5] #store the class start times in this list
    classJoinTimes = [8.35, 9.35, 10.85] #These are the comfort times, meaning if you run the bot betweeen the start time and this time it will join the class or else wait for the next class
    classEndTimes = [8.95 , 9.95 , 11.45 ]#these are the end times for all the classes meaning the times at which the bot is supposed to leave the respective classes
    
    #Please note that the times are in hours and not in hh:mm format for 8:30 is 8.5
    
    #google class room links for all the classes 
    classLinkList = ["https://classroom.google.com/c/MTM2ODQ0MjA5OTU4" , "https://classroom.google.com/c/MTM2ODQ0MjA5OTY3", "https://classroom.google.com/c/MTM2ODQ0MjA5OTgx", "https://classroom.google.com/c/MTM2ODQ0MjA5OTc0" , "https://classroom.google.com/c/MTM2ODQ0MjA5OTM3"]
    
    while True: #enters the infiinite loop

        #getting the day
        today = dayToday()
        print(today)
        if(today == "Monday"):
            dayNumber = 0
        elif ( today == "Tuesday"):
            dayNumber = 1
        elif ( today == "Wednesday"):
            dayNumber = 2
        elif ( today == "Thursday"):
            dayNumber = 3
        elif ( today == "Friday"):
            dayNumber = 4
        elif ( today == "Saturday"):
            dayNumber = 5
        elif( today == "Sunday"):
            dayNumber = 6
        #getting the time
        hours, minutes = getTimeNow()
        currentClassIndex = -1


        #hours , minutes = 8 , 55 #remove this before running the program 
        """Please remove this shit before running the program """


        print ( hours , minutes , sep = ":")
        for i in range(len(classTimings)): #which class is next as per current time
            if ((60*hours) + minutes) <= (60 * classJoinTimes[i]):
                currentClassIndex = i
                break
        
        if(currentClassIndex == -1): #checking if we are not already too late
            print("Its too late to join the class now my friend so take a chill pill and Dont worry its UNDERSTANDABLE HAVE A GREAT DAY")
            break
        timetableClassIndex =  3 * dayNumber + currentClassIndex #the constant 3 tells us that there are 3 classes for me in a day
        className = timetable[timetableClassIndex]
        if className == "Physics":
            link = classLinkList[0]
        elif className == "Chemistry":
            link = classLinkList[1]
        elif className == "Maths":
            link = classLinkList[2]
        elif className == "Computer":
            link = classLinkList[3]
        elif className == "English":
            link = classLinkList[4]
        
        while ((60 * hours) + minutes) < ((60 * classTimings[currentClassIndex]) +  2): #The constant  2 here is the offset for how later do you want the bot to join the class after it has started, for example currently it will join the class 2 minutes after the start time
            sleep(2) #time interval after which it will check whether Its time for the class
            hours , minutes = getTimeNow()
            print("Waiting for the class to start")
            print(hours , minutes , sep = ":")
        driver = webdriver.Chrome("E:/coding projects/chromedriver.exe")
        driver.set_window_position(0,0)
        driver.set_window_size(800, 800)
        driver.get("https://www.gmail.com")
        sleep(1)
        element = driver.find_element_by_name("identifier")
        element.send_keys("YourGmailID") #edit this to enter your Gmail ID for your google account
        element.send_keys(Keys.RETURN)
        sleep(2)    
        element = driver.find_element_by_name("password")
        element.send_keys("GmailPassword")#edit this to enter the password to your google account
        element.send_keys(Keys.RETURN)
        sleep(2)
        print(className)
        needToGoToClass = True
        while needToGoToClass: #keep stuck in this loop bitch till the meeting has not already started
            needToGoToClass = False
            driver.get(link)
            sleep(2)
            element = driver.find_elements_by_partial_link_text("meet.google")
            while(len(element) ==0):
                print("The class link is still not there" , getTimeNow())
                element = element = driver.find_elements_by_partial_link_text("meet.google")
                sleep(5)
            print("the meet link: " , element[0].text)
            driver.get(element[0].text)
            print(driver.title)
            if(driver.title == "Something went wrong"):
                needToGoToClass = True
                sleep(30)
        action  = ActionChains(driver)
        sleep(2)
        action.send_keys(Keys.RETURN)
        sleep(1)
        pyautogui.click(325,199)
        sleep(1)
        pyautogui.click(328,178)
        sleep(1)
        action.key_down(Keys.CONTROL).send_keys('e').key_up(Keys.CONTROL).perform()
        sleep(1)
        pyautogui.click(360 , 387)
        sleep(1)
        pyautogui.click(358, 646)
        sleep(1)
        hours , minutes = getTimeNow()
        endHours = 60 * classEndTimes[currentClassIndex]
        print("EndTime: " , (endHours//60) , (endHours%60))
        pyautogui.click(672, 146)
        message = client.messages.create(from_='whatsapp:+14155238886',
        body='Boss, I just joined ' + className +  ' class, at: ' + str(hours) +":"+ str(minutes),    
        to='whatsapp: YourWhatsapp number if you want a ping')
        print(message.status)
        print(message.sid)
        while( (60*hours)+ minutes < (60*classEndTimes[currentClassIndex])):
            print("class is going on")
            hours , minutes = getTimeNow()
            print(hours,  minutes, sep = ":")
            text = detectAudio() #chat button: 672 , 146 | name of chatbox = chatTextInput | 
            
            #the following if statements check for specific phrases in the translated text so that the bot can reply accordingly
            
            if  "is it clear" in text or "are you there" in text or "did all of you understand" in text or "did each one of you understand" in text or "are you getting it" in text or "did you all understand" in text or "did you understand" in text or "understood" in text :
                element = driver.find_elements_by_name("chatTextInput")
                if className == "Computer":
                    reply = "yes maam"
                else:
                    reply = "yes sir"
                print(len(element))
                if(len(element) == 0):
                    print("could not send reply because you didnt want me to")
                else: 
                    try: 
                        element[0].send_keys(reply)
                        element[0].send_keys(Keys.ENTER)
                        print("Sending reply:", reply )
                        del element
                    except:
                        print("could not send reply because you didnt want me to")
            

            if "any doubt" in text or "any problems" in text:
                element = driver.find_elements_by_name("chatTextInput")
                if className == "Computer":
                    reply = "no maam, no doubt"
                else:
                     reply = "no sir, no doubt"
                print(len(element))
                if(len(element) == 0):
                    print("could not send reply because you didnt want me to")
                else: 
                    try: 
                        element[0].send_keys(reply)
                        element[0].send_keys(Keys.ENTER)
                        print("Sending reply:", reply )
                        del element
                    except:
                        print("could not send reply because you didnt want me to")


            
            if "completed or not" in text or "have you all completed" in text or "are you writing " in text  or "are you still writing" in text or "writing or not writing" in text:
                element = driver.find_elements_by_name("chatTextInput")
                if className == "Computer":
                    reply = "yes maam completed"
                else:
                     reply = "yes sir completed"
                print(len(element))
                if(len(element) == 0):
                    print("could not send reply because you didnt want me to")
                else: 
                    try: 
                        element[0].send_keys(reply)
                        element[0].send_keys(Keys.ENTER)
                        print("Sending reply:", reply )
                        del element
                    except:
                        print("could not send reply because you didnt want me to")



            if "got it" in text or "are you getting it" in text:
                element = driver.find_elements_by_name("chatTextInput")
                if className == "Computer":
                    reply = "yes maam got it"
                else:
                     reply = "yes sir got it"
                print(len(element))
                if(len(element) == 0):
                    print("could not send reply because you didnt want me to")
                else: 
                    try: 
                        element[0].send_keys(reply)
                        element[0].send_keys(Keys.ENTER)
                        print("Sending reply:", reply )
                        del element
                    except:
                        print("could not send reply because you didnt want me to")


        
            if("thank you sir" in text or "leave class" in text or "leave the class" in text):
                break
        driver.get("https://www.google.com")
        driver.close() 