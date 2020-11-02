#!/usr/bin/env python3
#Author: Aaron Lee
#Title: stringReplacer
#Purpose: To Replace Strings in multiple Files
#Python version: 3.8.6 64-bit
#FOR TESTING PURPOSES
#LAPTOP-B1P29PK\SQLEXPRESS2016
#Janmo_POS_db
import os, json

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

def fileReplace(stringChangeDS, currentStringDS, stringChangeDB, currentStringDB, filename):
    # Read in the file
    with open(filename, 'r', encoding='utf-8') as file :
        filedata = file.read()
    # Replace the target string with the new string
    filedata = filedata.replace(currentStringDS, stringChangeDS)
    filedata = filedata.replace(currentStringDB, stringChangeDB)
    # Write the file out again
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(filedata)

def setup():
    loc0 = "MainFnB/App.ini"
    loc1 = "MecWise.JobServiceV4/Jobs/connectInfo.config"
    loc2 = "MecWise.JobServiceV4/Jobs/MecWise.JobLauncherV41.exe.config"
    loc3 = "C:/MecWisePOS/MecWisePOS.exe.config"
    print("Introduction: Autoscript for F&B software by Aaron Lee!")
    print("Version: 1.0")
    print("Instructions:\nDeploy this script in the directory \'D:\\\' drive")
    print("\nPlease check if local directory path is correct:\n"+loc0+"\n"+loc1+"\n"+loc2+"\n"+loc3)
    userInput = input("Press enter to continue...")
    os.system("cls")
    userInput = ""
    while userInput == "":
        userInput = input("What is the name of the data source?(Example: DESKTOP-B5PK6DK\SQLEXPRESS2008)\n")
    stringChangeDS = userInput
    userInput = ""
    userInput = input("\nWhat is the name of the data source in the config file?\nLeave input blank to use default values (Default: DESKTOP-B5PK6DK\SQLEXPRESS2008)\n")
    if userInput == "":
        currentStringDS = "DESKTOP-B5PK6DK\SQLEXPRESS2008"
    else:
        currentStringDS = userInput
    print(currentStringDS)
    userInput = ""
    while userInput == "":
        userInput = input("\nWhat is the name of the current database?(Example: FnB_Pos_Demo)\n")
    stringChangeDB = userInput
    userInput = ""
    userInput = input("\nWhat is the name of the current database in the config file?\nLeave input blank to use default values(Default: FnB_Pos_Demo)\n")
    if userInput == "":
        currentStringDB = "FnB_Pos_Demo"
    else:
        currentStringDB = userInput
    fileReplace(stringChangeDS, currentStringDS, stringChangeDB, currentStringDB, loc0)
    fileReplace(stringChangeDS, currentStringDS, stringChangeDB, currentStringDB, loc1)
    fileReplace(stringChangeDS, currentStringDS, stringChangeDB, currentStringDB, loc2)
    fileReplace(stringChangeDS, currentStringDS, stringChangeDB, currentStringDB, loc3)

def run():

def main():

main()

