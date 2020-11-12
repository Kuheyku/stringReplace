#!/usr/bin/env python3
#Author: Aaron Lee
#Title: Search and Replace program
#Purpose: To search and replace replace strings in multiple files
#Python version: 3.8.6 64-bit
#Program version: 1.1
#FOR TESTING PURPOSES
#LAPTOP-B1P29PK\SQLEXPRESS2016
#Janmo_POS_db
import json, os, time

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

def fileReplace(currentString, stringChange, filename):
    try:
        # Read in the file
        with open(filename, 'r', encoding='utf-8') as file :
            filedata = file.read()
        # Replace the target string with the new string
        filedata = filedata.replace(currentString, stringChange)
        # Write the file out again
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(filedata)
    except Exception as e:
        print("[ERROR] fileReplace function: " + e)

# This function will append dictionary key:value into the router list
def appendList(instanceName, currentStringList, changeStringList, pathLocationList, data):
    data['instance'].append({
        "instanceName": instanceName,
        "currentStringList": currentStringList,
        "changeStringList": changeStringList,
        "pathLocationList": pathLocationList
    })
    return data

def setup():
    # 1. Check whether a config file is present if not intialize variables accordingly
    try:
        data = openConfig()
    except:
        data = {}
        data["instance"] = []
    currentStringList = []
    changeStringList = []
    pathLocationList = []
    userInput = ""
    while userInput == "":
        userInput=input("Please input the name of this replace string instance\n")
    instanceName = userInput
    # 2. Ask for current string/text to be replaced with new string/text
    while userInput != "":
        userInput=input("Please input the string/text to be replaced. [CASE-SENSITIVE]\n(Leave input empty if there is none left to change)\n")
        if userInput != "":
            currentStringList.append({"string":userInput})
            userInput = ""
            while userInput == "":
                userInput=input("Please input in the new string/text to be replacing that string/text. [CASE-SENSITIVE]\n")
            changeStringList.append({"string":userInput})
    userInput = "init"
    # 3. Ask for file pathnames to apply changes to
    while userInput != "":
        userInput=input("Please input the path name of the files for the changes to be applied to. [CASE-SENSITIVE]\n(Leave input empty if there is no files left to apply changes to)\n")
        if userInput != "":
            pathLocationList.append({"path":userInput})

    writeToConfig(appendList(instanceName, currentStringList, changeStringList, pathLocationList, data))

def runMenu():
    os.system('cls')
    try:
        data = openConfig()
        currentInstance = 0
        choice = 0
        instanceAmt = len(data["instance"])
        print("Total of ("+str(instanceAmt)+") search and replace instance(s) found!\nInstance names:")
        for x in data["instance"]:
            instanceName = data["instance"][currentInstance]["instanceName"]
            print("("+str(currentInstance+1)+") "+instanceName)
            currentInstance = currentInstance + 1
        # Ask user for their intention
        userInput=int(input("\nPlease input the number next to the instance you wish to run.\nInput ("+str(instanceAmt+1)+") to run all instances.\nChoice: "))
    except Exception as e:
        print(e)
        print("[ERROR] Config file not found. Ensure a file named \'config.json\' is present in the same directory.")
        time.sleep(1)
        main()
        
    while choice == 0:
        if userInput >= 1 and userInput <= instanceAmt:
            run(userInput-1)
            break
        elif userInput == (instanceAmt+1):
            #Runs all
            run(userInput)
            break
        else:
            runMenu()
            break

def run(inputInstance):
    os.system('cls')
    currentInstance = inputInstance
    try:
        data = openConfig()
        instanceAmt = len(data["instance"])
        # Runs all instances
        if currentInstance > instanceAmt:
            currentInstance = 0
            print("Running string search & replace for all (" +str(instanceAmt)+ ") instances.")
            for x in data["instance"]:
                try:
                    # First it initializes all the variables
                    instanceName = data["instance"][currentInstance]["instanceName"]
                    currentStringList = data["instance"][currentInstance]["currentStringList"]
                    changeStringList = data["instance"][currentInstance]["changeStringList"]
                    pathLocationList = data["instance"][currentInstance]["pathLocationList"]
                    print("\nRunning string search & replace for instance: " + instanceName)
                    pointer = len(currentStringList) - 1
                    pointerPath = len(pathLocationList) - 1
                    while pointerPath >= 0:
                        try:
                            while pointer >= 0:
                                fileReplace(currentStringList[pointer]["string"], changeStringList[pointer]["string"], pathLocationList[pointerPath]["path"])
                                pointer = pointer - 1
                            print("[SUCCESS] Changes for " + pathLocationList[pointerPath]["path"] + " made successfully")
                        except:
                            print("[ERROR]" + pathLocationList[pointerPath]["path"] + " not found")
                        pointer = len(currentStringList) - 1
                        pointerPath = pointerPath - 1
                    currentInstance = currentInstance + 1    
                except Exception as e:
                    print(e)
                    print("[ERROR] Config file is corrupted. Please ensure all variables are correct in the file named \'config.json\' present in the same directory.\nIf error persists please delete \'config.json\' and re-setup.")
        else:
            try:
                # First it initializes all the variables
                instanceName = data["instance"][currentInstance]["instanceName"]
                currentStringList = data["instance"][currentInstance]["currentStringList"]
                changeStringList = data["instance"][currentInstance]["changeStringList"]
                pathLocationList = data["instance"][currentInstance]["pathLocationList"]
                print("Running string search & replace for instance: " + instanceName)
                pointer = len(currentStringList) - 1
                pointerPath = len(pathLocationList) - 1
                while pointerPath >= 0:
                    try:
                        while pointer >= 0:
                            fileReplace(currentStringList[pointer]["string"], changeStringList[pointer]["string"], pathLocationList[pointerPath]["path"])
                            pointer = pointer - 1
                        print("[SUCCESS] Changes for " + pathLocationList[pointerPath]["path"] + " made successfully")
                    except:
                        print("[ERROR]" + pathLocationList[pointerPath]["path"] + " not found")
                    pointer = len(currentStringList) - 1
                    pointerPath = pointerPath - 1
            except Exception as e:
                print(e)
                print("[ERROR] Instance values in the Config file is corrupted. Please ensure all variables are correct in the file named \'config.json\' present in the same directory.\nIf error persists please delete \'config.json\' and re-setup.")

    except Exception as e:
        print(e)
        print("[ERROR] Config file not found. Ensure a file named \'config.json\' is present in the same directory.")

def main():
    os.system('cls')
    choice = 0
    print("Introduction: Light-weight search and replace for multiple files Program")
    print("Author: Aaron Lee")
    print("Program version: 1.1")
    while choice == 0:
        # Ask user for their intention
        userInput=input("\nPlease pick a function\n(1) Setup\\Add new string replace instance\n(2) Run stored string replace instance\nChoice: ")
        if userInput == "1":
            setup()
            break
        elif userInput == "2":
            runMenu()
            break
        else:
            print("Invalid Input!")

main()