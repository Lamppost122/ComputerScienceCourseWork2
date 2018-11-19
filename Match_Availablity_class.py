

"""

Match availablity Class

This is the to tool set for sending out match availablity

"""

import re,datetime,io,sys,os.path,os,smtplib,hashlib, uuid,ctypes,imaplib
import smtplib
import time
import imaplib
import email
##from email.MIMEMultipart import MIMEMultipart
##from email.MIMEText import MIMEText
import tkinter as tk
from tkinter import font  as tkfont
from System_Tool_Kit import *
"""

        For Testing i am changing the all outward email address to be ComputerScienceTest2@gmail.com( line 30)

"""


class avilablity(playerDatabase):
    def emailMessage(self):
        text = "Are you avialable to play for Whitchurch "+teamNumber+ "'s ? "+"  \n"+" Date: "+ day + "\n"+"Time: " +time +"\n"+ "Location: " + location

        html = """\
<html>
  <head></head>
   <body>
   <code></code>
   <form class = "gform" method = "POST" data-email = "ComputerScienceTest1@gmail.com" action = "https://script.google.com/macros/s/AKfycbz3y9PRV1ovO5jqJa6N6MRC74bkBFRYLr0kSLd5CSA2yGOaSnaO/exec" >
  <input type="radio" name="Button" value="Yes """ +str(location)+str(time)+str(day)+str(opposition)+str(teamNumber)+str(email)+ """" checked> Yes<br>
  <input type="radio" name="Button" value="No  """ +str(location)+str(time)+str(day)+str(opposition)+str(teamNumber)+str(email)+""""> No<br>
  <input type="submit" value="Submit">

  </body>
</html>
"""
    body = text + html
    return body




    def sendAvilabilityCheck(self,location,time,day,opposition,teamNumber,email):

            email = "ComputerScienceTest2@gmail.com"
            msg = MIMEMultipart()
            text =  emailMessage()
            msg['Subject'] = "Whitchurch Hockey club availablity"
            msg.attach(MIMEText(body, 'html'))
            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("ComputerScienceTest1@gmail.com", "Password1@")
            server.sendmail("ComputerScienceTest1@gmail.com", email, text)
            server.quit()
            print(location+time+day+opposition+teamNumber+email)

    def getWeeksMatches(self):
        MatchWriter = open("WeeksMatches.txt",'w+')
        searchlines = readFile("matchFile.txt",'r')
        nextWeek = self.getNextWeek()
        for i, line in enumerate(searchlines):
            for j in nextWeek:
                if line[43:51] == j:
                    MatchWriter.write(line)

    def readEmailSetup(self):
        ORG_EMAIL   = "@gmail.com"
        FROM_EMAIL  = "ComputerScienceTest1" + ORG_EMAIL
        FROM_PWD    = "Password1@"
        SMTP_SERVER = "imap.gmail.com"
        SMTP_PORT   = 993
        return FROM_EMAIL,FROM_PWD,SMTP_SERVER,SMTP_PORT


    def read_Email(self):
        FROM_EMAIL,FROM_PWD,SMTP_SERVER,SMTP_PORT = readEmailSetup()

        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        CreateInbox(latest_email_id,first_email_id,data)

    def CreateInbox(latest_email_id,first_email_id,data):

        inbox = []

        for currentEmail in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(currentEmail, '(RFC822)' )
            inbox.append(FindSubject(data))

        return inbox


    def FindSubject(self,data):

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1])
                email_subject = msg['subject']
                Emails =email_subject[12:120]
                return Emails




    def matchResponces(self,time,day,teamNumber):
        inbox =  self.read_Email()

        respondedPlayer = []
        for k, email in enumerate(inbox):

            if email[34:47] == str(time+day):
                searchlines = readFile("team"+str(teamNumber)+".txt",'r')
                for j ,data in enumerate(searchlines):

                    if email[78:].lstrip() in data:

                        Player = data[5:35].strip()+data[35:65].strip()
                        PlayerResponce = email[:5]
                        respondedPlayer.append(str(ResponceType(respondedPlayer,Player,PlayerResponce)+"  " +Player))




        return respondedPlayer

    def ResponceType(self,respondedPlayer,Player,PlayerResponce):

        if "Yes" in PlayerResponce:
            Responce ="Yes"
        else:
            Responce ="No"
        return Responce



    def getNextWeek(self):
        nextWeek=[]
        for j in range(7):
            today = (datetime.date.today() + datetime.timedelta(days=j)).strftime("%d/%m/%y")
            nextWeek.append(today)
        return nextWeek

    def emailList(self,teamNumber):

        self.getWeeksMatches()
        weeksMatches = readFile("WeeksMatches.txt",'r')
        for i, matches in enumerate(weeksMatches):

            if teamNumber == matches[5:8].lstrip("0"):
                location,time,day,opposition = matchDataFormat(matches)


                Check = ctypes.windll.user32.MessageBoxA(0,  ("Is Whitchurch " + teamNumber +"'s vs "+opposition.strip()+" on the "+day +" the match your looking for ?"),"Search", 4)

                if Check ==6:
                    return location,time,day,opposition

    def matchDataFormat(self,matches):
        location = matches[8:38]
        time = matches[38:43]
        day = matches[43:51]
        opposition = matches[51:81]
        return location,time,day,opposition



    def sendEmailGroup(self,location,time,day,opposition,teamNumber):
        File2 = open("Team"+str(teamNumber)+".txt","r")
        searchLines = File2.readlines()
        for j, players in enumerate(searchLines):
            email = players[65:95]
            self.sendAvilabilityCheck(location,time,day,opposition,teamNumber,email)





