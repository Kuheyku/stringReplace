#!/usr/bin/env python3
# Author : Aaron May 2020
# Program Name: DeTech Password Changer
# Version: 1.1.3
# To configure the password changer to suit different routers
# prequsite : firefox webdriver : geckodriver
# to install :
# download the corresponding gz file from https://github.com/mozilla/geckodriver/releases
# unzip the file to get the geckodriver.
# copy this binary to /usr/local/bin
# that's it.

import socket, struct, time, sqlite3, functools, operator, datetime, hashlib, codecs, json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def getSeleniumDriver():
    options = Options()
    options.headless = True
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument('--ignore-certificate-errors')
    options.binary_location = "/usr/bin/chromium"
    #driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    return driver

# This function will return with default gateway value
def getDefGateway():
    # Read the default gateway directly from /proc.
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue
            fh.close()
            return str(socket.inet_ntoa(struct.pack("<L", int(fields[2], 16))))
# This function will append dictionary key:value into the router list
def appendList(secretkey, name, wait, gateway, pwpage, username, usernameElement, pw, pwElement, elementList, pwElementList, applyElement, applyWait, data):
    data['router'].append({
        "secretkey": secretkey,
        "name": name,
        "waitTime": wait,
        "routerGateway": gateway,
        "loginPage": pwpage,
        "username": username,
        "usernameElement": usernameElement,
        "password": pw,
        "passwordElement": pwElement,
        "elementList": elementList,
        "passwordElementList": pwElementList,
        "applyElement": applyElement,
        "applyWait": applyWait
    })
    return data
# This function will write values to the config.json
def writeToConfig(dataAdd):
    with open("config.json", "w") as outfile:
        json.dump(dataAdd, outfile, indent=2)
        outfile.close()
def openConfig():
    #Try to open "config.json" file in current directory
    with open("config.json") as configFile:
        data = json.load(configFile)
        configFile.close()
    return data
# This function handles clearing, then inputting values into element fields, it takes the driver, element name/id, the value you wish to send in, boolean for Keys.RETURN and wait interval
def elemSendKey(driver, element, value, keyReturn, wait):
    time.sleep(wait)
    isPresent = len(driver.find_elements_by_name(element)) > 0
    if isPresent:
        elem = driver.find_element_by_name(element)
        elem.clear()
        elem.send_keys(value)
    else:
        isPresent = len(driver.find_elements_by_id(element)) > 0
        if isPresent:
            elem = driver.find_element_by_id(element)
            elem.clear()
            elem.send_keys(value)
        else:
            print(element + ": No element found(maybe set your wait time longer)")
    if keyReturn == True:
        try:
            elem.send_keys(Keys.RETURN)
        except Exception as e:
            print(e)
# This function handles clicking of elements, it takes the driver, element name/id/linktext and wait interval
def elemClick(driver, element, wait):
    time.sleep(wait)
    isPresent = len(driver.find_elements_by_name(element)) > 0
    if isPresent:
        driver.find_element_by_name(element).click()
    else:
        isPresent = len(driver.find_elements_by_id(element)) > 0
        if isPresent:
            driver.find_element_by_id(element).click()
        else:
            isPresent = len(driver.find_elements_by_link_text(element)) > 0
            if isPresent:
                driver.find_element_by_link_text(element).click()
            else:
                print(element + ": No element found(maybe set your wait time longer)")
def newPw(input1):
    now=datetime.datetime.now()
    date = now.strftime('%Y-%m-%d') #year month daate format
    str1 = date+input1
    hash=hashlib.sha256(str1.encode('utf-8')).hexdigest()
    b64 = codecs.encode(codecs.decode(hash, 'hex'), 'base64').decode().strip()
    newpass = b64[0:12]
    return newpass
def setup(configPresent):
    if configPresent == False:
        data = {}
        data["router"] = []
        routerAmt = 0
    else:
        data = openConfig()
        routerAmt = len(data["router"])
    elementList = []
    pwElementList = []
    # 1.1 Ask for secret key
    userInput = ""
    while userInput == "":
        userInput=input("Please type in the secret key(required): ")
        if userInput != "":
            secretkey = userInput
    # 1.2 Ask for name of router
    userInput=input("Please type in the name of this router(It can be anything): ")
    if userInput == "":
        name = "Router " + str(routerAmt + 1)
    else:
        name = userInput
    print("Name of router: " + name)
    # 1.3 Ask for wait time
    userInput = ""
    userInput=input("Please enter the wait interval in seconds, this is for the browser to load before an action(default: 1s): ")
    if userInput == "":
        wait = 1
    else:
        wait = int(userInput)
    # 2.1. Ask for webpage that changes password
    userInput=input("Please enter the router's gateway address(Leave it empty to use default: " + getDefGateway() + "): ")
    gateway = userInput
    if gateway == "":
        gateway = str(getDefGateway())
    # 2.1. Ask for webpage that changes password
    userInput=input("Please type in the path to the router's firmware webpage that handles logins:\n" + gateway + "/").lower()
    pwpage = userInput
    # 2.2. Acess the webpage
    try:
        loginpage = "http://"+ gateway + "/" + pwpage
        print("Trying to access "+ loginpage)
        driver = getSeleniumDriver()
        driver.get(loginpage)
    except Exception as e:
        print(e)
    # 3.1. Ask for username
    userInput=input("Please type in the username(Leave it empty if there is no username field): ")
    username = userInput
    # 3.2. Ask for username element name/id, only when a username field is present, if not set usernameElement to empty
    if username != "":
        userInput=input("Please type in the element name/id of username field: ")
        usernameElement = userInput
        elemSendKey(driver, usernameElement, username, False, wait)
    else:
        usernameElement = ""
    # 4.1. Ask for password
    userInput=input("Please type in the password: ")
    pw = userInput
    # 4.2. Ask for password element name/id
    userInput=input("Please type in the element name/id of password field: ")
    pwElement = userInput
    elemSendKey(driver, pwElement, pw, True, wait)
    # 5. Ask for element ID's to navigate to password change
    while userInput != "":
        userInput=input("Please type in the element name(s)/id(s) or hyperlink link text to navigate to the change password page(Leave it empty if there is none needed)\nElement name/id or hyperlink link text: ")
        if userInput != "":
            elemClick(driver, userInput, wait)
            elementList.append({"element":userInput})
    # 6. Ask for change password element name
    print("DeTech-Password Changer supports multiple change password fields.\n")
    userInput = "init before loop"
    while userInput != "":
        userInput=input("Please type in the element name(s)/id(s) of the change password fields(Leave it empty if there is none needed)\nElement name/id: ")
        if userInput != "":
            elemSendKey(driver, userInput, newPw(secretkey), False, wait)
            pwElementList.append({"element":userInput})
    # 7. Ask for confirm/apply button element to change password
    userInput=input("Please type in the element name(s)/id(s) or hyperlink link text of confirm/apply button to change the password\nElement name/id or hyperlink link text: ")
    applyElement = userInput
    # 8. Ask for apply wait time
    userInput = ""
    userInput=input("Some router firmwares take a while before changes are applied.\nPlease enter the wait interval in seconds, this is to wait for the rounter to finish apply changes(default: 6s): ")
    if userInput == "":
        applyWait = 6
    else:
        applyWait = int(userInput)
    # 9. Ask whether user would like to change password during set up phase
    userInput=input("Do you wish to change the password during set up?\nPlease pick a function\n(1) Yes, (2) No, Default: No\nChoice: ")
    if userInput == "1":
        elemClick(driver, applyElement, wait)
        time.sleep(applyWait)
    # hohphootah
    # Writes to the config file
    writeToConfig(appendList(secretkey, name, wait, gateway, pwpage, username, usernameElement, pw, pwElement, elementList, pwElementList, applyElement, applyWait, data))
    print("Configuration for " + name + " has been successfully initialised.\nPress Enter to continue...")
    try:
        driver.close()
    except:
        print("Webpage was closed by the user.")

def run():
    data = openConfig()
    routerAmt = len(data["router"])
    currentRouter = 0
    for x in data["router"]:
        try:
            # First it intilizes all the variables
            secretkey = data["router"][currentRouter]["secretkey"]
            name = data["router"][currentRouter]["name"]
            wait = data["router"][currentRouter]["waitTime"]
            gateway = data["router"][currentRouter]["routerGateway"]
            pwpage = data["router"][currentRouter]["loginPage"]
            username = data["router"][currentRouter]["username"]
            usernameElement = data["router"][currentRouter]["usernameElement"]
            pw = data["router"][currentRouter]["password"]
            pwElement = data["router"][currentRouter]["passwordElement"]
            elementList = data["router"][currentRouter]["elementList"]
            pwElementList = data["router"][currentRouter]["passwordElementList"]
            applyElement = data["router"][currentRouter]["applyElement"]
            applyWait = data["router"][currentRouter]["applyWait"]
            # Here is where the application runs
            try:
                loginpage = "http://"+ gateway + "/" + pwpage
                print("Trying to access "+ loginpage)
                driver = getSeleniumDriver()
                driver.get(loginpage)
            except Exception as e:
                print(e)
            # Handles sending in of username if any
            if username != "":
                elemSendKey(driver, usernameElement, username, False, wait)
            # Handles sending in of password
            elemSendKey(driver, pwElement, pw, True, wait)
            print("Login Successful!")
            # For every dictionary in the list execute elemClick
            for x in elementList:
                elemClick(driver, x["element"], wait)
            print("Located change password page...")
            # For every dictionary in the list execute elemSendKey
            for x in pwElementList:
                elemSendKey(driver, x["element"], newPw(secretkey), False, wait)
            print("Password(s) changed...")
            elemClick(driver, applyElement, wait)
            print("Applying changes for "+name+"...")
            time.sleep(applyWait)
            print("Password change process for " + name + " has been successfully completed.\nPress Enter to continue...")
            driver.close()
            currentRouter = currentRouter + 1
        except:
            print("Config File corrupted, please remove it and initalise again.")
        input("Password change process for " + str(routerAmt) + " routers has been successfully completed.\nPress Enter to exit...")

def choice():
    j = 0
    while j == 0:
        # Ask user for their intention
        userInput=input("Welcome user to the password changer configurator\nPlease pick a function\n(1) Add new router\n(2) Run password changer\nChoice: ")
        if userInput == "1":
            setup(True)
            break
        elif userInput == "2":
            print("Run Password Changer")
            run()
            break
        else:
            print("Invalid Input!")

def main():
    try:
        i = 0
        data = openConfig()
        routerAmt = len(data["router"])
        print("Config file found.\nNo. of router configurations: " + str(routerAmt))
        for x in data["router"]:
            i = i + 1
            print (str(i) + ". " + x["name"])
        print("")
        # Ask user for their intention
        choice()
    except Exception as e:
        print(e)
        print("Config file does not exist.\nAssuming initialisation of password changer configuration...\n")
        setup(False)
main()