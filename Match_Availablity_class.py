

"""

Match availablity Class

This is the to tool set for sending out match availablity

"""

import re,datetime,io,sys,os.path,os,smtplib,hashlib, uuid,ctypes
##from email.MIMEMultipart import MIMEMultipart
##from email.MIMEText import MIMEText
import tkinter as tk
from tkinter import font  as tkfont

class avilablity():

    def sendAvilabilityCheck(self,location,time,day,opposition,teamNumber,email):
            msg = MIMEMultipart()
            body = "Are you avialable to play for Whitchurch "+teamNumber+ "'s ? \nDate: "+ day + "\nTime: " +time + "Location: " + Location
            msg['Subject'] = "Whitchurch Hockey club availablity"
            msg.attach(MIMEText(body, 'plain'))
            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("ComputerScienceTest1@gmail.com", "Password1@")
            server.sendmail("ComputerScienceTest1@gmail.com", email, text)
            server.quit()

    def getWeeksMatches(self):
        File = open("matchFile.txt",'r')
        searchlines = File.readlines()
        nextWeek = self.getNextWeek()
        matchs = []
        for i, line in enumerate(searchlines):
            for j in nextWeek:
                if line[43:53] == j:
                    print(line)

                    matchs.append(line)
        return matchs



    def getNextWeek(self):
        i = datetime.datetime.now()
        today = "%s" % (i)
        today = today[8:10] +"/"+ today[5:7]+"/" +today[0:4]
        nextWeek=[]
        for j in range(7):
            nextWeek.append(today)
            today = today[0]+str(int(today[1])  +1 )+today[2:]

        return nextWeek

    def emailList(self):
        matchList = self.getWeeksMatches()
        for i in matchList:
            teamNumber = i[7:8]
            File = open("team"+teamNumber+".txt",'r')
            searchlines = File.readlines()
            for j, line in enumerate(searchlines):
                email = line[65:95].strip()
                location = i[8:38].strip()
                time = i[38:42]
                day = i[42:52]
                opposition = i[52:82].strip()
                self.sendAvilabilityCheck(self,location,time,day,opposition,teamNumber,email)

