

"""
Player Database class

This is the tool set for creating the system

This system should be designed to be highly flexable

Note:
    The key tool in this the remove and search tools
    Need to improve the search system. This could be achieved by creating a new screen with tk.
    Need to clear out unnessecary lines

"""

import re,datetime,io,sys,os.path,os,smtplib,hashlib, uuid,ctypes
##from email.MIMEMultipart import MIMEMultipart
##from email.MIMEText import MIMEText
import tkinter as tk
from tkinter import font  as tkfont


class playerDatabase:

    def init__Database():
        database = open(playerDatabase,'w+')
        database.close()

    def remove(self,sourceFile,lineCount):

        File = open(sourceFile,'r')
        searchlines = File.readlines()
        Temp = open("ComputerSceinceTemp.txt",'w+')
        subLineCount =0
        for j, line in enumerate(searchlines):
            subLineCount += 1
            if lineCount != subLineCount:
                Temp.write(str(line))
        Temp.close()
        File = open(sourceFile,'w')
        Temp = open("ComputerSceinceTemp.txt","r")
        for line in Temp:
            File.write(line)
        Temp.close()
        File.close()
        os.remove("ComputerSceinceTemp.txt")


    def search(self,sourceFile,find1,find2,find3,searchType):
        File = open(sourceFile,'r')
        searchlines = File.readlines()
        found = []
        lineCount = 0

        for i, line in enumerate(searchlines):
            if find1 in line and find2 in line and find3 in line:

                for l in searchlines[i:i+1]:
                    found.append(l),

        for j in found:
            lineCount +=1

            Check = ctypes.windll.user32.MessageBoxA(0,  (self.message(j,searchType) ),"Search", 4)

            if Check ==6:
                return lineCount,j

    def message(self,j,searchType):
        if searchType == "player":
            message = j[5:65].split()
            message = "Is "+message[0].capitalize() + " "+ message[1].capitalize() +" the Player your looking for ? (y/n)"
            return message
        if searchType == "match":
            message = "Is Whitchurch " + j[7:8]+"'s vs "+j[53:].strip()+" on the "+j[43:53] +" the match your looking for ? (y/n)"
            return message
        if searchType == "team":
            message = j[5:65].split()
            message ="Is "+ message[0].capitalize() + " "+ message[1].capitalize()+" the Player your looking for ? (y/n)"
            return message
        if searchType == "addPlayer":
            message = j[5:65].split()
            message ="Is "+ message[0].capitalize() + " "+ message[1].capitalize()+" the Player you want to add ? (y/n)"
            return message

    def searchByFirstName(self):
        find1 = raw_input("Search by first name for : ")
        lineCount,j = self.search('playerDatabase.txt',find1,"","","player")
        return j

    def searchByLastName(self):
        find1 = raw_input("Search by last name for : ")
        lineCount,j = self.search('playerDatabase.txt',find1,"","","player")
        return j

    def addMatch(self):
        m1=match("","","","","","")
        matchFile = open("matchFile.txt",'a+')
        matchFile.write(m1.getMatchData()+"\n")
        matchFile.close()

    def removeMatch(self):
        find1 =raw_input("Who is the opposition ?")
        find2 = raw_input("What team is playing ?")
        lineCount,j =self.search(find1,find2,"","match")
        self.remove("matchFile.txt",lineCount)

    def editMatch(self):
        find1=raw_input("What match would you like to edit ?")
        lineCount,playerEdit = self.search("matchFile.txt",find1,"","","match")
        editFeature = raw_input("What would you like to edit ? \nlocation time day opposition")
        if editFeature =="location":
            change = raw_input("What you you like to change the location to ? ")
            change = "{:<30}".format(change)
            playerEdit = playerEdit.replace(str(playerEdit[8:38]),str(change))
        if editFeature =="time":
            change = raw_input("What you you like to change the time to ? ")
            playerEdit = playerEdit.replace(str(playerEdit[38:43]),str(change))
        if editFeature =="day":
            change = raw_input("What you you like to change the day to ? ")
            playerEdit = playerEdit.replace(str(playerEdit[43:53]),str(change))
        if editFeature =="opposition":
            change = raw_input("What you you like to change the opposition to ? ")
            change = "{:<30}".format(change)
            playerEdit = playerEdit.replace(str(playerEdit[53:83]),str(change))
        self.remove("matchFile.txt",lineCount)
        database = open("matchFile.txt",'a')
        database.write(playerEdit)
        database.close()
