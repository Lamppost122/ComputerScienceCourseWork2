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
from Data_Import import *


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)


        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login, Register, Home, EditPlayerDatabase,AddPlayer, removePlayer,EditPlayerDetailsBottom,EditPlayerDetailsTop,EditTeams,CreateTeam,EditMatch,addMatch,Import,playerImport,matchImport,TeamList,MatchAvailablity):
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
        self.EditMatchButton = tk.Button(self, text="Edit Match ",command=lambda: controller.show_frame("EditMatch") )
        self.ImportButton = tk.Button(self, text="Import files",command=lambda: controller.show_frame("Import") )
        self.TeamListButton = tk.Button(self, text="Produce a team list",command=lambda: controller.show_frame("TeamList") )
        self.MatchAvailablityButton = tk.Button(self, text="Match Availability",command=lambda: controller.show_frame("MatchAvailablity") )
        self.Title = tk.Label(self, text="Please select a function", font=controller.title_font)

        self.Title.grid(row=0,column=0,columnspan=3)
        self.EditPlayerButton.grid(row=1,column=0)
        self.EditTeamButton.grid(row=1,column=1)
        self.EditMatchButton.grid(row =1,column =2)
        self.ImportButton.grid(row = 2,column = 0)
        self.TeamListButton.grid(row = 2,column = 1)
        self.MatchAvailablityButton.grid(row = 2, column = 2)


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
        self.lblFirstNameError= tk.Label(self)
        self.lblLastNameError= tk.Label(self)
        self.lblEmailError= tk.Label(self)
        self.lblPhoneNumberError= tk.Label(self)
        self.lblAddressError= tk.Label(self)
        self.lblPostcodeError= tk.Label(self)
        self.lblDateOfBirthError= tk.Label(self)

        self.SubmitButton= tk.Button(self, text="Submit",command=lambda: self.addPlayer() )
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
        self.lblFirstNameError.grid(row=1,column=2)
        self.lblLastNameError.grid(row=2,column=2)
        self.lblEmailError.grid(row=3,column=2)
        self.lblPhoneNumberError.grid(row=4,column=2)
        self.lblAddressError.grid(row=5,column=2)
        self.lblPostcodeError.grid(row=6,column=2)
        self.lblDateOfBirthError.grid(row=7,column=2)
        self.SubmitButton.grid(row=8,column=0,columnspan=2)
        self.BackButton.grid(row=9,column = 0,columnspan = 2)

    def addPlayer(self):
        playerID = self.getPlayerID()
        dateOfJoining = self.getDateOfJoining()
        firstName = self.getFirstName(self.txtFirstName.get())
        lastName=self.getLastName(self.txtLastName.get())
        email = self.getEmail(self.txtEmail.get())
        phoneNumber = self.getPhoneNumber(self.txtPhoneNumber.get())
        dateOfBirth = self.getDateOfBirth(self.txtDateOfBirth.get())
        address = self.getAddress(self.txtAddress.get())
        postcode = self.getPostcode(self.txtPostcode.get())

        playerData = self.getPlayerData(playerID,firstName,lastName,email,phoneNumber,address,postcode,dateOfBirth,dateOfJoining)
        i,validation = self.validData(firstName,lastName,email,phoneNumber,address,postcode,dateOfBirth)


        if validation != True:
            i,validation = self.validData(firstName,lastName,email,phoneNumber,address,postcode,dateOfBirth)

        else:

            database = open("playerDatabase.txt",'a+')
            database.write(str(playerData) + "\n")
            database.close()
        #self.controller.show_frame("Home")


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

        self.AddTeamButton = tk.Button(self, text="Create Team",command=lambda: self.teamCreation(controller) )
        self.RemoveRemoveButton = tk.Button(self, text="Remove Player",command=lambda: controller.show_frame("removeTeam") )
        self.EditTeamButton = tk.Button(self, text="Edit Player Details",command=lambda: controller.show_frame("EditPlayerTeamTop") )
        self.BackButton= tk.Button(self, text="Back",command=lambda: controller.show_frame("Home"))

        self.AddTeamButton.grid(row=1,column=0)
        self.RemoveRemoveButton.grid(row=1,column=1)
        self.EditTeamButton.grid(row=1,column=2)
        self.BackButton.grid(row=4,column = 0,columnspan = 3)

    def teamCreation(self,controller):
        teamNumber = 1
        while True:
            if os.path.isfile("team"+str(teamNumber)+".txt") == True:
                 int(teamNumber)
                 teamNumber += 1


            else:
                teamFile = open("team"+str(teamNumber)+".txt",'w+')
                break
        controller.show_frame("CreateTeam")





class CreateTeam(tk.Frame,playerDatabase):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        teamNumber = 1
        while True:
            if os.path.isfile("team"+str(teamNumber)+".txt") == True:
                 int(teamNumber)
                 teamNumber += 1


            else:

                break



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
        self.BackButton = tk.Button(self, text="Back",command=lambda: self.backButton(teamNumber,controller) )
        self.FinnishButton = tk.Button(self, text="Finnish",command=lambda: self.finnishButton(controller) )

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
        self.BackButton.grid(row=4,column = 0)
        self.FinnishButton.grid(row=4,column =1)



    def addPlayerToTeam(self,teamNumber):
        AddSearchValue = self.AddSearchPlayer.get()

        if AddSearchValue != "":

            teamFile = open("team"+str(teamNumber)+".txt",'a+')

            lineCount,j = self.search('playerDatabase.txt',AddSearchValue,"","","addPlayer")

            teamFile.write(str(j)+"\n")
            j = j[5:35].strip() +" "+ j[35:65].strip()
            self.table.insert(1,j)
            teamFile.close()




    def removePlayerFromTeam(self,teamNumber,find1):
        if find1 !="":


            lineCount = self.search(find1,"","","team")
            self.remove("team"+str(teamNumber)+".txt",lineCount)

    def backButton(self,teamNumber,controller):

        os.remove("team"+str(teamNumber)+".txt")
        controller.show_frame("EditTeams")

    def finnishButton(self,controller):
        controller.show_frame("EditTeams")

class EditMatch(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.AddMatchButton = tk.Button(self, text="Add Match",command=lambda: controller.show_frame("addMatch") )
        self.RemoveMatchButton = tk.Button(self, text="Remove Match",command=lambda: controller.show_frame("removeTeam") )
        self.EditMatchButton = tk.Button(self, text="Edit Match Details",command=lambda: controller.show_frame("EditPlayerTeamTop") )
        self.BackButton= tk.Button(self, text="Back",command=lambda: controller.show_frame("Home"))

        self.AddMatchButton.grid(row=1,column=0)
        self.RemoveMatchButton.grid(row=1,column=1)
        self.EditMatchButton.grid(row=1,column=2)
        self.BackButton.grid(row=4,column = 0,columnspan = 3)


class addMatch(tk.Frame,match):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.lblTeam= tk.Label(self,text="Team: ")
        self.lblLocation =tk.Label(self,text="Location: ")
        self.lblTime = tk.Label(self,text="Time: ")
        self.lblDay = tk.Label(self,text="Day: ")
        self.lblOpposition = tk.Label(self,text="Opposition: ")
        self.txtTeam = tk.Entry(self)
        self.txtLocation = tk.Entry(self)
        self.txtTime = tk.Entry(self)
        self.txtDay = tk.Entry(self)
        self.txtOpposition = tk.Entry(self)

        self.lblTeam.grid(row=0,column=0)
        self.lblLocation.grid(row=1,column=0)
        self.lblTime.grid(row=2,column=0)
        self.lblDay.grid(row=3,column=0)
        self.lblOpposition.grid(row=4,column=0)
        self.txtTeam.grid(row = 0,column = 1)
        self.txtLocation.grid(row = 1,column = 1)
        self.txtTime.grid(row = 2,column = 1)
        self.txtDay.grid(row = 3,column = 1)
        self.txtOpposition.grid(row = 4,column = 1)




        self.BackButton = tk.Button(self, text="Back",command=lambda: controller.show_frame("EditMatch") )
        self.SaveButton = tk.Button(self, text="Save",command=lambda: self.saveButton(controller) )
        self.BackButton.grid(row=5,column =0)
        self.SaveButton.grid(row=5,column =1)

    def saveButton(self,controller):

        Team = self.getTeamNumber(self.txtTeam.get())
        Location = self.getLocation(self.txtLocation.get())
        Time = self.getTime(self.txtTime.get())
        Day = self.getDay(self.txtDay.get())
        Opposition =self.getOpposition( self.txtOpposition.get())
        MatchID = self.getMatchID()
        Match = MatchID+Team+Location+Time+Day+Opposition+"\n"
        File = open("matchFile.txt","a+")
        File.write(Match)

        controller.show_frame("EditTeams")

class Import(tk.Frame,match,DataImport):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.PlayerImportButton = tk.Button(self, text="Import Players",command=lambda: controller.show_frame("playerImport") )
        self.MatchImportButton = tk.Button(self, text="Import Match",command=lambda: self.saveButton(controller) )
        self.BackButton = tk.Button(self, text="Back",command=lambda: controller.show_frame("Home") )
        self.PlayerImportButton.grid(row=0,column =0)
        self.MatchImportButton.grid(row=0,column =1)
        self.BackButton.grid(row=1,column =1)

class playerImport(tk.Frame,match,DataImport):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        lblFile = tk.Label(self,text = "What is the address of the file you want to import ?")
        self.txtImportFile = tk.Entry(self)
        ImportButton = tk.Button(self,text="Import",command=lambda: self.Button(controller))
        BackButton = tk.Button(self, text="Back",command=lambda: controller.show_frame("Import") )
        lblFile.grid(row = 0 ,column =0)
        self.txtImportFile.grid(row = 0,column =1 )
        BackButton.grid(row =1,column =0)
        ImportButton.grid(row= 1,column =1 )



    def Button(self,controller):
        file = self.txtImportFile.get()
        if file != "":
            self.PlayerImport(file)
            controller.show_frame("Import")

class matchImport(tk.Frame,match,DataImport):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        lblFile = tk.Label(self,text = "What is the address of the file you want to import ?")
        txtImportFile = tk.Entry(self)
        ImportButton = tk.Button(self,text="Import",command=lambda: self.Button(controller))
        BackButton = tk.Button(self, text="Back",command=lambda: controller.show_frame("Import") )
        lblFile.grid(row = 0 ,column =0)
        txtImportFile.grid(row = 0,column =1 )
        BackButton.grid(row =1,column =0)
        ImportButton.grid(row= 1,column =1 )



    def Button(self,controller):
        file = self.txtImportFile.get()
        if file != "":
            self.MatchImport(file)
            controller.show_frame("Import")

class TeamList(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        teamNumber =1


        while True:

            if os.path.isfile("team"+str(teamNumber)+".txt") == True:
                 int(teamNumber)
                 teamNumber += 1

            else:
                break

        tableWidth = 3
        teamNumber = teamNumber//tableWidth

        currentTeam = 0
        for i in range(teamNumber+1):
            for m in range(tableWidth):
                currentTeam = currentTeam+1
                if os.path.isfile("team"+str(currentTeam)+".txt") == False:
                    break
                self.lblTable = tk.Label(self,text = "Team" + str(currentTeam))
                self.table = tk.Listbox(self)
                n = 2*int(i)
                File = open("Team" + str(i*m+1)+".txt",'r+')
                searchlines = File.readlines()

                for j, line in enumerate(searchlines):
                    k = line[5:35].strip() +" "+ line[35:65].strip()
                    self.table.insert(1,k)
                self.lblTable.grid(row=n,column=m)
                self.table.grid(row = n+1,column=m)

class MatchAvailablity(tk.Frame,avilablity):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.location = ""
        self.time = ""
        self.day = ""
        self.opposition = ""
        self.teamNumber = 0
        self.lblTeamSelection = tk.Label(self,text = "Team: ")
        self.txtTeamSelection = tk.Entry(self)
        self.TeamSelectionButton = tk.Button(self,text = "Load Team",command=lambda: self.LoadTeam())

        self.table = tk.Listbox(self)

        self.lblMatchSelection = tk.Label(self,text = "Match : ")
        self.txtTeamSelection = tk.Entry(self)
        self.MatchSelectionButton = tk.Button(self,text = "Select Match",command=lambda: self.MatchSelection())
        self.SendEmailButton = tk.Button(self,text = "Send Email",command  = lambda:self.sendEmailGroup(self.location,self.time,self.day,self.opposition,self.teamNumber))
        self.SeeResponcesButton = tk.Button(self,text = "See Responces",command=lambda: self.SeeResponces())
        self.table = tk.Listbox(self)
        self.ResponceTable = tk.Listbox(self)

        self.lblTeamSelection.grid(row =0, column = 0 )
        self.txtTeamSelection.grid(row=0,column = 1)
        self.TeamSelectionButton.grid(row = 1,column = 1)
        self.table.grid(row =1,column=0,)
        self.lblMatchSelection.grid(row = 2 ,column = 0)
        self.SendEmailButton.grid(row = 3, column = 0)
        self.MatchSelectionButton.grid(row=2,column =1 )
        self.SeeResponcesButton.grid(row = 4,column = 1)
        self.ResponceTable.grid(row = 4,column = 0)

    def MatchSelection(self):
        self.teamNumber = self.txtTeamSelection.get()
        if self.teamNumber !="":
            self.location,self.time,self.day,self.opposition = self.emailList(self.teamNumber)
            self.lblMatchSelection.config(text = str("Match : Whitchurch " + self.teamNumber +"'s vs "+self.opposition.strip()+" on the "+self.day)  )
        else:
            print("You have not enter at team number")





    def LoadTeam(self):
        teamNumber = self.txtTeamSelection.get()
        if teamNumber != "" :
            File = open("Team" + str(teamNumber)+".txt",'r+')
            searchlines = File.readlines()

            for j, line in enumerate(searchlines):
                k = line[5:35].strip() +" "+ line[35:65].strip()
                self.table.insert(1,k)


    def SeeResponces(self):
        Responces = self.matchResponces(self.time,self.day,self.teamNumber)
        for i in Responces:
            self.ResponceTable.insert(1,i)







if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
