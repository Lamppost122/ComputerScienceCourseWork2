
"""

Gui

This is the system that handles Gui

"""

import re,datetime,io,sys,os.path,os,smtplib,hashlib, uuid,ctypes
##from email.MIMEMultipart import MIMEMultipart
##from email.MIMEText import MIMEText
import tkinter as tk
from tkinter import font  as tkfont

from Player_class import *
from System_Tool_Kit import *
from Team_Class import *
from Match_Class import *
from Match_Availablity_class import *


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)


        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login, Register, Home, EditPlayerDatabase,AddPlayer, removePlayer,EditPlayerDetailsBottom,EditPlayerDetailsTop,EditTeams,CreateTeam):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class Login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.Title = tk.Label(self, text="Please login to your account", font=controller.title_font)
        self.loginButton = tk.Button(self, text="Login",command= lambda: checkDetails(self))
        self.registerButton = tk.Button(self, text="Register",command=lambda: controller.show_frame("Register"))
        self.lblUsername = tk.Label(self,text="Username: ")
        self.lblPassword = tk.Label(self,text="Password: ")
        self.txtUsername = tk.Entry(self)
        self.txtPassword = tk.Entry(self)

        self.txtUsername.grid(row=1,column = 1)
        self.txtPassword.grid(row=2,column = 1)
        self.loginButton.grid(row=3,column=1)
        self.registerButton.grid(row=3,column=0)
        self.lblUsername.grid(row=1,column=0)
        self.lblPassword.grid(row=2,column=0)
        self.Title.grid(row=0,column=0,columnspan=2)


        def checkDetails(self):
            File = open("users.txt",'r+')
            searchlines = File.readlines()
            username = self.txtUsername.get()
            password = self.txtPassword.get()
            for i, line in enumerate(searchlines):
                if username in line[5:35]:

                    salt1 =163
                    salt2 = 195
                    hashed1 = 35
                    hashed2 = 163
                    salt = line[salt1:salt2]
                    searchPassword = line[hashed1:hashed2]
                    if  searchPassword == hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest():
                        controller.show_frame("Home")




class Register(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.Title = tk.Label(self, text="Please fill in your details", font=controller.title_font)
        self.loginButton = tk.Button(self, text="Login",command=lambda: controller.show_frame("Login") )
        self.registerButton = tk.Button(self, text="Register",command=lambda: self.register())
        self.lblUsername = tk.Label(self,text="Username: ")
        self.lblPassword = tk.Label(self,text="Password: ")
        self.lblConfirmUsername = tk.Label(self,text="Confirm Username: ")
        self.lblConfirmPassword = tk.Label(self,text="Confirm Password: ")
        self.lblEmail = tk.Label(self,text="Email: ")
        self.txtUsername = tk.Entry(self)
        self.txtConfirmUsername = tk.Entry(self)
        self.txtPassword = tk.Entry(self)
        self.txtConfirmPassword = tk.Entry(self)
        self.txtEmail = tk.Entry(self)


        self.txtUsername.grid(row=1,column = 1)
        self.txtConfirmUsername.grid(row=2,column = 1)
        self.txtPassword.grid(row=3,column = 1)
        self.txtConfirmPassword.grid(row=4,column = 1)
        self.txtEmail.grid(row=5,column = 1)
        self.loginButton.grid(row=6,column = 1)
        self.registerButton.grid(row=6,column = 0)
        self.lblUsername.grid(row=1,column = 0)
        self.lblConfirmUsername.grid(row=2,column = 0)
        self.lblPassword.grid(row=3,column = 0)
        self.lblConfirmPassword.grid(row=4,column = 0)
        self.lblEmail.grid(row=5,column = 0)
        self.Title.grid(row=0,column = 0,columnspan=2)

    def register(self):
        username =  self.txtUsername.get()
        confirmUsername = self.txtConfirmUsername.get()
        password = self.txtPassword.get()
        confirmPassword = self.txtConfirmPassword.get()
        Email = self.txtEmail.get()


        if username == confirmUsername and password == confirmPassword and username !="" and password !="" and Email !="" :
            File = open("users.txt",'a+')
            if self.validUsername(username) == True:
                salt = uuid.uuid4().hex
                hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
                userID = sum(1 for line in open("users.txt")) + 1
                userID = "{:05d}".format(userID)
                username = "{:<30}".format(username)
                Email =  "{:<60}".format(Email)
                userID= str(userID)

                File.write(userID+username+hashed_password+salt+Email)
                File.close()
                self.controller.show_frame("Home")



    def validUsername(self,username):
        File = open("users.txt",'r+')
        searchlines = File.readlines()
        for i, line in enumerate(searchlines):
            if username in line[5:35]:
                return False
                File.close()
                break

        return True
        File.close()




class Home(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.EditPlayerButton = tk.Button(self, text="Edit Player ",command=lambda: controller.show_frame("EditPlayerDatabase") )
        self.EditTeamButton = tk.Button(self, text="Edit Team ",command=lambda: controller.show_frame("EditTeams") )
        self.Title = tk.Label(self, text="Please select a function", font=controller.title_font)

        self.Title.grid(row=0,column=0,columnspan=3)
        self.EditPlayerButton.grid(row=1,column=0)
        self.EditTeamButton.grid(row=1,column=1)


class   EditPlayerDatabase(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.AddPlayerButton = tk.Button(self, text="Add Player",command=lambda: controller.show_frame("AddPlayer") )
        self.RemovePlayerButton = tk.Button(self, text="Remove Player",command=lambda: controller.show_frame("removePlayer") )
        self.EditPlayerDetailsButton = tk.Button(self, text="Edit Player Details",command=lambda: controller.show_frame("EditPlayerDetailsTop") )
        self.BackButton= tk.Button(self, text="Back",command=lambda: controller.show_frame("Home"))

        self.AddPlayerButton.grid(row=1,column=0)
        self.RemovePlayerButton.grid(row=1,column=1)
        self.EditPlayerDetailsButton.grid(row=1,column=2)
        self.BackButton.grid(row=4,column = 0,columnspan = 3)


class   AddPlayer(tk.Frame,playerDatabase,player):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.lblFirstName= tk.Label(self,text=" First Name :")
        self.lblLastName= tk.Label(self,text=" Last Name :")
        self.lblEmail= tk.Label(self,text="  Email:")
        self.lblPhoneNumber= tk.Label(self,text=" Phone Number :")
        self.lblAddress= tk.Label(self,text=" Address :")
        self.lblPostcode= tk.Label(self,text=" Postcode :")
        self.lblDateOfBirth= tk.Label(self,text=" Date of Birth :")
        self.txtFirstName = tk.Entry(self)
        self.txtLastName = tk.Entry(self)
        self.txtEmail = tk.Entry(self)
        self.txtPhoneNumber = tk.Entry(self)
        self.txtAddress = tk.Entry(self)
        self.txtPostcode = tk.Entry(self)
        self.txtDateOfBirth = tk.Entry(self)

        firstName = self.getFirstName(self.txtFirstName.get())
        lastName=self.getLastName(self.txtLastName.get())
        email = self.getEmail(self.txtEmail.get())
        phoneNumber = self.getPhoneNumber(self.txtPhoneNumber.get())
        dateOfBirth = self.getDateOfBirth(self.txtDateOfBirth.get())
        address = self.getAddress(self.txtAddress.get())
        postcode = self.getPostcode(self.txtPostcode.get())

        self.SubmitButton= tk.Button(self, text="Submit",command=lambda: self.addPlayer(firstName,lastName,email,phoneNumber,dateOfBirth,address,postcode) )
        self.BackButton= tk.Button(self, text="Back",command=lambda: controller.show_frame("EditPlayerDatabase"))

        self.lblFirstName.grid(row=1,column=0)
        self.lblLastName.grid(row=2,column=0)
        self.lblEmail.grid(row=3,column=0)
        self.lblPhoneNumber.grid(row=4,column=0)
        self.lblAddress.grid(row=5,column=0)
        self.lblPostcode.grid(row=6,column=0)
        self.lblDateOfBirth.grid(row=7,column=0)
        self.txtFirstName.grid(row=1,column=1)
        self.txtLastName.grid(row=2,column=1)
        self.txtEmail.grid(row=3,column=1)
        self.txtPhoneNumber.grid(row=4,column=1)
        self.txtAddress.grid(row=5,column=1)
        self.txtPostcode.grid(row=6,column=1)
        self.txtDateOfBirth.grid(row=7,column=1)
        self.SubmitButton.grid(row=8,column=0,columnspan=2)
        self.BackButton.grid(row=9,column = 0,columnspan = 2)

    def addPlayer(self,firstName,lastName,email,phoneNumber,dateOfBirth,address,postcode):
        playerID = self.getPlayerID()
        dateOfJoining = self.getDateOfJoining()
        playerData = str(playerID+firstName+lastName+email+phoneNumber+address+postcode+dateOfBirth+dateOfJoining)
        database = open("playerDatabase.txt",'a+')
        database.write(playerData + "\n")
        database.close()
        self.controller.show_frame("Home")


class removePlayer(tk.Frame,playerDatabase):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.lblSearch= tk.Label(self,text=" Search for player to remove :")
        self.txtSearch = tk.Entry(self)
        self.lblSearch.grid(row=1,column=0)
        self.txtSearch.grid(row=2,column=0)

        Search = self.txtSearch.get()
        self.SearchButton= tk.Button(self, text="Search",command=lambda: self.removePlayer(Search) )
        self.BackButton= tk.Button(self, text="Back",command=lambda: controller.show_frame("EditPlayerDatabase"))

        self.SearchButton.grid(row=3,column =0 ,columnspan = 2 )
        self.BackButton.grid(row=4,column = 0,columnspan = 2)



    def removePlayer(self,find1):

        lineCount,j = self.search("playerDatabase.txt",find1,"","","player")
        self.remove("playerDatabase.txt",lineCount)
        self.controller.show_frame("Home")

class EditPlayerDetailsTop(tk.Frame,playerDatabase):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.lblSearch= tk.Label(self,text=" Search for player to edit :")
        self.txtSearch = tk.Entry(self)

        Search = self.txtSearch.get()

        self.SearchButton= tk.Button(self, text="Search",command=lambda: self.EditPlayerSearch(Search) )
        self.BackButton= tk.Button(self, text="Back",command=lambda: controller.show_frame("EditPlayerDatabase"))

        self.lblSearch.grid(row=1,column=0)
        self.txtSearch.grid(row=2,column=0)
        self.SearchButton.grid(row=3,column =0 ,columnspan = 2 )
        self.BackButton.grid(row=4,column = 0,columnspan = 2)

    def EditPlayerSearch(self,search):
         lineCount,searchResult = self.search("playerDatabase.txt",search,"","","player")
         self.controller.show_frame("EditPlayerDetailsBottom")
         return lineCount



class EditPlayerDetailsBottom(tk.Frame,playerDatabase):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.lblFirstName= tk.Label(self,text=" First Name :")
        self.lblLastName= tk.Label(self,text=" Last Name :")
        self.lblEmail= tk.Label(self,text="  Email:")
        self.lblPhoneNumber= tk.Label(self,text=" Phone Number :")
        self.lblAddress= tk.Label(self,text=" Address :")
        self.lblPostcode= tk.Label(self,text=" Postcode :")
        self.lblDateOfBirth= tk.Label(self,text=" Date of Birth :")
        self.txtFirstName = tk.Entry(self)
        self.txtLastName = tk.Entry(self)
        self.txtEmail = tk.Entry(self)
        self.txtPhoneNumber = tk.Entry(self)
        self.txtAddress = tk.Entry(self)
        self.txtPostcode = tk.Entry(self)
        self.txtDateOfBirth = tk.Entry(self)
        self.EditButton= tk.Button(self, text="Edit",command=lambda: self.editPlayer() )
        self.BackButton= tk.Button(self, text="Back",command=lambda: controller.show_frame("EditPlayerDetailsTop"))

        self.lblFirstName.grid(row=1,column=0)
        self.lblLastName.grid(row=2,column=0)
        self.lblEmail.grid(row=3,column=0)
        self.lblPhoneNumber.grid(row=4,column=0)
        self.lblAddress.grid(row=5,column=0)
        self.lblPostcode.grid(row=6,column=0)
        self.lblDateOfBirth.grid(row=7,column=0)
        self.txtFirstName.grid(row=1,column=1)
        self.txtLastName.grid(row=2,column=1)
        self.txtEmail.grid(row=3,column=1)
        self.txtPhoneNumber.grid(row=4,column=1)
        self.txtAddress.grid(row=5,column=1)
        self.txtPostcode.grid(row=6,column=1)
        self.txtDateOfBirth.grid(row=7,column=1)
        self.EditButton.grid(row=8,column=0,columnspan=2)
        self.BackButton.grid(row=9,column = 0,columnspan = 2)

    def editPlayer(self):
        firstName = self.txtFirstName.get()
        lastName=self.txtLastName.get()
        email = self.txtEmail.get()
        phoneNumber = self.txtPhoneNumber.get()
        dateOfBirth = self.txtDateOfBirth.get()
        address = self.txtAddress.get()
        postcode = self.txtPostcode.get()

        lineCount,searchResult = self.search("playerDatabase.txt","","","","player")
        playerEdit = searchResult

        if firstname !="":
            change = firstname
            change = "{:<30}".format(change)
            playerEdit = playerEdit.replace(str(playerEdit[5:35]),str(change))
        if lastname !="":
            change = lastname
            change = "{:<30}".format(change)
            playerEdit = playerEdit.replace(str(playerEdit[35:65]),str(change))
        if email !="":
            change =email
            change = "{:<30}".format(change)
            playerEdit = playerEdit.replace(str(playerEdit[65:95]),str(change))
        if phoneNumber !="":
            change = phoneNumber
            change = "{:<11}".format(change)
            playerEdit = playerEdit.replace(str(playerEdit[95:106]),str(change))
        if address !="":
            change = address
            change = "{:<30}".format(change)
            playerEdit = playerEdit.replace(str(playerEdit[106:136]),str(change))
        if postcode !="":
            change = postcode
            change = "{:<8}".format(change)
            playerEdit = playerEdit.replace(str(playerEdit[136:144]),str(change))
        if dateOfBirth =="":
            change = dateOfBirth
            playerEdit = playerEdit.replace(str(playerEdit[144:154]),str(change))


        self.remove("playerDatabase.txt",lineCount)
        database = open("playerDatabase.txt",'a')
        database.write(playerEdit+"\n")
        database.close()

        teamNumber = 1
        while True:
            if os.path.isfile("team"+str(teamNumber)+".txt") == True:

                searchlines = File.readlines()

                lineCount = 0

                for i, line in enumerate(searchlines):
                    lineCount +=1
                    if searchResult == line:
                        self.remove("team"+str(teamNumber)+".txt",lineCount)
                        database = open("team"+str(teamNumber)+".txt",'a')
                        database.write(playerEdit+"\n")
                        database.close()
                        break
                teamNumber += 1
            else:
                break

class EditTeams(tk.Frame,playerDatabase):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.AddTeamButton = tk.Button(self, text="Create Team",command=lambda: controller.show_frame("CreateTeam") )
        self.RemoveRemoveButton = tk.Button(self, text="Remove Player",command=lambda: controller.show_frame("removeTeam") )
        self.EditTeamButton = tk.Button(self, text="Edit Player Details",command=lambda: controller.show_frame("EditPlayerTeamTop") )
        self.BackButton= tk.Button(self, text="Back",command=lambda: controller.show_frame("Home"))

        self.AddTeamButton.grid(row=1,column=0)
        self.RemoveRemoveButton.grid(row=1,column=1)
        self.EditTeamButton.grid(row=1,column=2)
        self.BackButton.grid(row=4,column = 0,columnspan = 3)

class CreateTeam(tk.Frame,playerDatabase):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        teamNumber = 1
##        while True:
##            if os.path.isfile("team"+str(teamNumber)+".txt") == True:
##                 int(teamNumber)
##                 teamNumber += 1
##            else:
##                break


        self.lblTeam = tk.Label(self,text = ("Team "+str(teamNumber) ))
        self.lblAddPlayer = tk.Label(self,text = "Add Player")
        self.lblPlayer1 = tk.Label(self,text = "Player :")
        self.AddSearchPlayer = tk.Entry(self)
        self.lblRemovePlayer = tk.Label(self,text = "Remove Player")
        self.lblPlayer2 = tk.Label(self,text = "Player :")
        self.RemoveSearchPlayer = tk.Entry(self)
        self.table = tk.Listbox(self)


        RemoveSearchVaule =self.RemoveSearchPlayer.get()

        self.AddPlayerButton = tk.Button(self, text="Add",command=lambda: self.addPlayerToTeam(teamNumber) )
        self.RemovePlayerButton = tk.Button(self, text="Remove",command=lambda: self.addPlayerToTeam(teamNumber,RemoveSearchVaule) )

        self.lblAddPlayer.grid(row=0,column=0)
        self.lblTeam.grid(row=0,column=4)
        self.lblPlayer1.grid(row=1,column=0)
        self.AddSearchPlayer.grid(row=1,column=1)
        self.AddPlayerButton.grid(row=1,column=2)
        self.table.grid(row=2,column=1)
        self.lblRemovePlayer.grid(row=2,column=0)
        self.lblPlayer2.grid(row=3,column=0)
        self.RemoveSearchPlayer.grid(row=3,column=1)
        self.RemovePlayerButton.grid(row=3,column=2)
        self.table.grid(row=1,column=4,rowspan=4)



    def addPlayerToTeam(self,teamNumber):
        AddSearchValue = self.AddSearchPlayer.get()

        if AddSearchValue != "":

            teamFile = open("team"+str(teamNumber)+".txt",'a+')

            lineCount,j = self.search('playerDatabase.txt',AddSearchValue,"","","addPlayer")

            teamFile.write(str(j))
            j = j[5:35].strip() +" "+ j[35:65].strip()
            self.table.insert(1,j)
            teamFile.close()

    def removePlayerFromTeam(self,teamNumber,find1):
        if find1 !="":


            lineCount = self.search(find1,"","","team")
            self.remove("team"+str(teamNumber)+".txt",lineCount)



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
