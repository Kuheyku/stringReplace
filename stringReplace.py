#!/usr/bin/env python3
#Author: Aaron Lee
#Title: stringReplacer
#Purpose: To Replace Strings in multiple Files
#Python version: 3.8.6 64-bit
#Program version: 1.0
#FOR TESTING PURPOSES
#LAPTOP-B1P29PK\SQLEXPRESS2016
#Janmo_POS_db
import json

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
        print("[SUCCESS] Changes for "+filename + " made successfully")
    except:
        print("[ERROR]" +filename + " not found")

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
    choice = 0
    while choice == 0:
        # Ask user for their intention
        userInput=input("\nPlease pick a function\n(1) run string replace instance\n(2) Run all string replace instance\nChoice: ")
        if userInput == "1":
            main()
            break
        elif userInput == "2":
            runAll()
            break
        else:
            print("Invalid Input!")

def runAll():
    try:
        data = openConfig()
        currentInstance = 0
        for x in data["instance"]:
            try:
                # First it initializes all the variables
                instanceName = data["instance"][currentInstance]["instanceName"]
                currentStringList = data["instance"][currentInstance]["currentStringList"]
                changeStringList = data["instance"][currentInstance]["changeStringList"]
                pathLocationList = data["instance"][currentInstance]["pathLocationList"]
                print("Running string replace for instance:" + instanceName)
                pointer = len(currentStringList) - 1
                pointerPath = len(pathLocationList) - 1
                print(currentStringList[pointer]["string"])
                while pointer >= 0:
                    while pointerPath >= 0:
                        fileReplace(currentStringList[pointer]["string"], changeStringList[pointer]["string"], pathLocationList[pointerPath]["path"])
                        pointerPath = pointerPath - 1
                    pointerPath = len(pathLocationList) - 1
                    pointer = pointer - 1
                currentInstance = currentInstance + 1
            except Exception as e:
                print(e)
                print("[ERROR] Config file is corrupted. Please ensure all variables are correct in the file named \'config.json\' present in the same directory.\nIf error persists please delete \'config.json\' and set up all string replace instances.")
    except Exception as e:
        print(e)
        print("[ERROR] Config file not found. Ensure a file named \'config.json\' is present in the same directory.")

def main():
    choice = 0
    print("Introduction: Light-Weight String Replacer Program by Aaron Lee!")
    print("Program version: 1.0")
    while choice == 0:
        # Ask user for their intention
        userInput=input("\nPlease pick a function\n(1) Add new string replace instance\n(2) Run stored string replace instance\nChoice: ")
        if userInput == "1":
            setup()
            break
        elif userInput == "2":
            runMenu()
            break
        else:
            print("Invalid Input!")

main()

