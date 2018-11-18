

"""

Match availablity Class

This is the to tool set for sending out match availablity

"""

import re,datetime,io,sys,os.path,os,smtplib,hashlib, uuid,ctypes,imaplib
import smtplib
import time
import imaplib
import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import tkinter as tk
from tkinter import font  as tkfont
from System_Tool_Kit import *
"""

        For Testing i am changing the all outward email address to be ComputerScienceTest2@gmail.com( line 30)

"""


class avilablity(playerDatabase):



    def sendAvilabilityCheck(self,location,time,day,opposition,teamNumber,email):

            email = "ComputerScienceTest2@gmail.com"
            msg = MIMEMultipart()
            text = "Are you avialable to play for Whitchurch "+teamNumber+ "'s ? "+"  \n"+" Date: "+ day + "\n"+"Time: " +time +"\n"+ "Location: " + location
            body = text + """\
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
        File = open("matchFile.txt",'r')
        MatchWriter = open("WeeksMatches.txt",'w+')
        searchlines = File.readlines()
        nextWeek = self.getNextWeek()
        for i, line in enumerate(searchlines):
            for j in nextWeek:
                if line[43:51] == j:
                    MatchWriter.write(line)


    def read_Email(self):
        ORG_EMAIL   = "@gmail.com"
        FROM_EMAIL  = "ComputerScienceTest1" + ORG_EMAIL
        FROM_PWD    = "Password1@"
        SMTP_SERVER = "imap.gmail.com"
        SMTP_PORT   = 993
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        inbox = []

        for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)' )

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    Emails =email_subject[12:120]
                    inbox.append(Emails)



        return inbox

    def matchResponces(self,time,day,teamNumber):
        inbox =  self.read_Email()

        respondedPlayer = []
        for k, email in enumerate(inbox):

            if email[34:47] == str(time+day):
                File = open("team"+str(teamNumber)+".txt",'r')
                searchlines = File.readlines()
                for j ,data in enumerate(searchlines):

                    if email[78:].lstrip() in data:

                        Player = data[5:35].strip()+data[35:65].strip()
                        if "Yes" in email[:5]:
                            Responce ="Yes"
                            respondedPlayer.append(str(Responce+"  " +Player))

                        else:
                            Responce ="No"
                            respondedPlayer.append(str(Responce+"  " +Player))
        return respondedPlayer





    def getNextWeek(self):
        nextWeek=[]
        for j in range(7):
            today = (datetime.date.today() + datetime.timedelta(days=j)).strftime("%d/%m/%y")
            nextWeek.append(today)
        return nextWeek

    def emailList(self,teamNumber):

        self.getWeeksMatches()
        File = open("WeeksMatches.txt",'r')




        weeksMatches = File.readlines()
        File.close()
        for i, matches in enumerate(weeksMatches):

            if teamNumber == matches[5:8].lstrip("0"):

                location = matches[8:38]
                time = matches[38:43]
                day = matches[43:51]
                opposition = matches[51:81]
                Check = ctypes.windll.user32.MessageBoxA(0,  ("Is Whitchurch " + teamNumber +"'s vs "+opposition.strip()+" on the "+day +" the match your looking for ?"),"Search", 4)

                if Check ==6:
                    return location,time,day,opposition


    def sendEmailGroup(self,location,time,day,opposition,teamNumber):
        File2 = open("Team"+str(teamNumber)+".txt","r")
        searchLines = File2.readlines()
        for j, players in enumerate(searchLines):
            email = players[65:95]
            self.sendAvilabilityCheck(location,time,day,opposition,teamNumber,email)






