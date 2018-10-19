"""

Team class

This is the tool set for creating a team

Note:
    Need to clear out unnessecary lines that are gonna be used

"""
import re,datetime,io,sys,os.path,os,ctypes
from Player_class import *
from System_Tool_Kit import *

class team(player,playerDatabase):
    def __init__(self,player1,player2,player3,player4,player5,player6,player7,player8,player9,player10,player11,player12,player13,player14,player15,player16):
        self.player1 = player
        self.player2 = player
        self.player3 = player
        self.player4 = player
        self.player5 = player
        self.player6 = player
        self.player7 = player
        self.player8 = player
        self.player9 = player
        self.player10 = player
        self.player11 = player
        self.player12 = player
        self.player13 = player
        self.player14 = player
        self.player15 = player
        self.player16 = player

    def createTeam(self):
        teamNumber = 1
        while True:
            if os.path.isfile("team"+str(teamNumber)+".txt") == True:
                 int(teamNumber)
                 teamNumber += 1
            else:
                break
        teamFile = open("team"+str(teamNumber)+".txt",'w+')
        for i in range(16):
            teamFile.write(str(self.searchByFirstName()))
        teamFile.close()

    def addPlayerToTeam(self):
        teamNumber = raw_input("What team do add a player to ?")
        teamFile = open("team"+str(teamNumber)+".txt",'a+')
        find1 = raw_input("Search for :")
        lineCount,j = self.search('playerDatabase.txt',find1,"","","addPlayer")
        teamFile.write(str(j))
        teamFile.close()

    def removePlayerFromTeam(self):

        teamNumber = raw_input("What team do you want to edit ?")
        find1 =raw_input("Who do you want to remove")
        lineCount = self.search(find1,"","","team")
        self.remove("team"+str(teamNumber)+".txt",lineCount)


    def replacePlayerInTeam(self):
        teamNumber = raw_input("What team do you want to edit ?")
        find1 =raw_input("Who do you want to replace?")
        lineCount = self.search(find1,"","","team")
        self.remove("team"+str(teamNumber)+".txt",lineCount)
        teamFile = open("team"+str(teamNumber)+".txt",'a+')
        find1 = raw_input("Search for :")
        lineCount,j = self.search('playerDatabase.txt',find1,"","","addPlayer")
        teamFile.write(str(j))
        teamFile.close()
       
    def removeTeam(self,teamNumber):
        os.remove("team"+teamNumber+".txt")
