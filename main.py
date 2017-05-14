from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, NoSuchWindowException, NoSuchElementException
import os
import time
import sys
import json
import urllib.request
import shutil
import platform
import getpass
import string
loggedIn = False
oneQuiz = False
osSelected = False
osis = 0
# 0 = Mac, 1 = Windows, 2 = Linux
directory = os.getcwd()
platform = platform.system()
if (platform == "darwin"):
    osis = 0
if (platform == "win32"):
    osis = 1
if (platform == "linux" or platform == "linux32"):
    osis = 2
with open ('info.json', 'r') as myfile:
        info=json.loads(myfile.read())
pageID = info["pageID"]
successes = info["successes"]
failures = info["failures"]
path = info["path"]
username = info["username"]
password = info["password"]
checkedforchrome = False
def save(info, pageID1, successes1, failures1, path1, username1, password1):
    info["pageID"] = pageID1
    info["successes"] = successes1
    info["failures"] = failures1
    info["path"] = path1
    info["username"] = username1
    info["password"] = password1
    with open ('info.json', 'r+') as myfile:
        info=myfile.write(json.dumps(info))
if (path == "ns"):
    while (checkedforchrome == False):
        checkedforchrome = True
        chromecheck = input('Have you installed ChromeDriver (Y or N)? ')
        if (chromecheck == "y" or chromecheck == "Y"):
            opentype = input("Is it in the script's directory? ")
            if (opentype == "n" or opentype == "N"):
                path = input("The path to chromedriver is: ")
            if (opentype == "Y" or opentype == "y"):
                if osis == 0 or osis == 2:
                    path = directory+"/"+"chromedriver"
                if osis == 1:
                    path = directory+"/"+"chromedriver.exe"
            save(info, pageID, successes, failures, path, username, password)
            print("Continuing...")

        if (not chromecheck == "Y" and not chromecheck == "y" and not chromecheck == "N" and not chromecheck == "n"):
            print("Invalid Option...Restarting...")
            checkedforchrome = False

        if (chromecheck == "n" or chromecheck == "N"):
            chromeinstalled = input("Would you like the script to install it for you (Y or N)? ")
            if (chromeinstalled == "y" or chromeinstalled == "Y"):
                while (osSelected == False):
                    osSelected = True
                    useros = input("What OS are you on (W for Windows, M for Mac, L64 for 64 bit Linux, and L32 for 32 bit Linux)? ")
                    print("Downloading...")
                    if (useros == "w" or useros == "W"):
                        downloadurl = "https://chromedriver.storage.googleapis.com/2.29/chromedriver_win32.zip"
                        file_name = "chromedriver_win32.zip"
                    if (useros == "m" or useros == "M"):
                        downloadurl = "https://chromedriver.storage.googleapis.com/2.29/chromedriver_mac64.zip"
                        file_name = "chromedriver_mac64.zip"
                    if (useros == "l64" or useros == "L64"):
                        downloadurl = "https://chromedriver.storage.googleapis.com/2.29/chromedriver_linux64.zip"
                        file_name = "chromedriver_linux64.zip"
                    if (useros == "l32" or useros == "L32"):
                        downloadurl = "https://chromedriver.storage.googleapis.com/2.29/chromedriver_linux32.zip"
                        file_name = "chromedriver_linux32.zip"
                    if (not useros == "w" and not useros == "W" and not useros == "m" and not useros == "M" and not useros == "l64" and not useros == "L64" and not useros == "l32" and not useros == "L32"):
                        print("Invalid Option. Restarting...")
                        time.sleep(0.5)
                        osSelected = False
                    with urllib.request.urlopen(downloadurl) as response, open(file_name, 'wb') as out_file:
                        shutil.copyfileobj(response, out_file)
                    print("Downloaded! Please unzip the file and restart the script.")
                    time.sleep(1)
                    sys.exit()
            if (chromeinstalled == "n" or chromeinstalled == "N"):
                    print("Goodbye!")
                    sys.exit()
if (username == "ns" and password == "ns"):
        reply = input('Would you like to have the script enter your username and password for you (Y or N)? ')
        if (reply == "n" or reply == "N"):
            username == "dw"
            password == "dw"
        if (reply == "Y" or reply == "y"):
            print("None of this data is transmitted, it is just saved for ease of use on your local machine.")
            username = input("Email: ")
            password = getpass.getpass("Password: ")
        save(info, pageID, successes, failures, path, username, password)
        print("Thank you!")
print("INFO: Only close the browser, not the script or terminal")
runTypeSelected = False
while runTypeSelected == False:
    runTypeSelected = True
    print("Type in an option: Start, Reset Data, Quit")
    time.sleep(0.1)
    runTypeInput = input("I choose: ")
    time.sleep(0.1)
    runTypeInput = runTypeInput.upper()
    if runTypeInput == "START":
        chooseRunType = input("Would you like to do multiple quizes (Y or N)? ")
        if (chooseRunType == "y" or chooseRunType == "Y"):
            oneQuiz = False
        if (chooseRunType == "n" or chooseRunType == "N"):
            oneQuiz = True
    if runTypeInput == "RESET DATA":
        usersure = input("Are you sure (Y or N)? ")
        if (usersure == "y" or usersure == "Y"):
            # pageID = 0
            # successes = 0
            # failures = 0
            path = "ns"
            username = "ns"
            password = "ns"
            print("Resetting...")
            time.sleep(0.1)
            save(info, pageID, successes, failures, path, username, password)
            pageID = 0
            successes = 0
            failures = 0
            save(info, pageID, successes, failures, path, username, password)
            sys.exit()
            runTypeSelected = False
        if (usersure == "n" or usersure == "N"):
            runTypeSelected = False
    if runTypeInput == "QUIT":
        print("Goodbye!")
        sys.exit()
    if not runTypeInput == "START" and not runTypeInput == "RESET DATA" and not runTypeInput == "QUIT":
        runTypeSelected = False
chromedriver = path
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)
browser.set_window_size(1600, 1000)
def click(id):
    try:
        browser.find_element_by_id("definition-"+id).click()
        browser.find_element_by_id("term-"+id).click()
    except:
        pass
def login():
    try:
        browser.find_element_by_xpath("//div[@class='TrophiesModal-loggedOutActions']/div/button").click()
    except:
        browser.find_element_by_xpath("//a[@href][2]").click()
    time.sleep(2)
    browser.find_element_by_xpath("//div[@class='UISocialButton']/a").click()
    try:
        browser.find_element_by_xpath("//input[@type='email']").send_keys(username+Keys.ENTER)
        time.sleep(1)
        browser.find_element_by_xpath("//input[@type='password']").send_keys(password+Keys.ENTER)
    except:
        pass

if oneQuiz == False:
    while True:
        save(info, pageID, successes, failures, path, username, password)
        try:
            browser.get("https://quizlet.com/"+str(pageID)+"/micromatch")
            browser.find_element_by_id("start").click()
            terms = browser.find_elements_by_xpath("//a[@data-type='term']")
            for term in terms:
                click(term.get_attribute("data-id"))
            successes = successes + 1
            if not loggedIn:
                time.sleep(1)
                login()
                loggedIn = True
            pageID = pageID + 1
            time.sleep(2)
        except NoSuchWindowException:
            sys.exit()
        except WebDriverException as e:
            failures = failures + 1
            pageID = pageID + 1
        except NoSuchElementException:
            failures = failures + 1
            pageID = pageID + 1
        except:
            print("Failure...")
            pass
if oneQuiz == True:
    while True:
        save(info, pageID, successes, failures, path, username, password)
        try:
            browser.get("https://quizlet.com/"+str(pageID)+"/micromatch")
            browser.find_element_by_id("start").click()
            terms = browser.find_elements_by_xpath("//a[@data-type='term']")
            for term in terms:
                click(term.get_attribute("data-id"))
            successes = successes + 1
            if not loggedIn:
                login()
                loggedIn = True
            time.sleep(2)
        except NoSuchWindowException:
            sys.exit()
        except WebDriverException:
            sys.exit()
        except NoSuchElementException:
            failures = failures + 1
            pageID = pageID + 1
