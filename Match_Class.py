"""
Match class

This is the tool set for creating a match instance

Note:
    Need to remove unnessecary lines

"""
import re,datetime,io,sys,os.path,os,ctypes

from Player_class import *
from System_Tool_Kit import *
from Team_Class import *
from Match_Class import *
from Match_Availablity_class import *


class match(team):
    def __init__(self,matchID,teamNumber,location,time,day,opposition):
        self.matchID = self.getMatchID()
        self.teamNumber = self.getTeamNumber()
        self.location = self.getLocation()
        self.time = self.getTime()
        self.day = self.getDay()
        self.opposition = self.getOpposition()

    def getMatchID(self):
        File = open("matchFile.txt","r")
        data = File.readlines()


        if len(data) != 0 :
            data =  str(data[-1])
            matchID=int(data[0:5])+1
            matchID = "{:05d}".format(matchID)
            matchID = str(matchID)
        else:
            matchID = "00001"

        return matchID

    def getTeamNumber(self,teamNumber):
        self.teamNumber = str(teamNumber)
        self.teamNumber = "{:03d}".format(int(self.teamNumber))
        self.teamNumber = str(self.teamNumber)
        return self.teamNumber

    def getLocation(self,Location):
        self.location = Location
        if len(self.location) > 30 :
            self.getLocation()
        self.location = "{:<30}".format(self.location)
        self.location.lower()
        return self.location

    def getTime(self,time):

        return time

    def getDay(self,day):

        return day

    def getOpposition(self,opposition):
        self.opposition = opposition
        if len(self.opposition) > 30 :
            self.getOpposition()
        self.opposition = "{:<30}".format(self.opposition).lower()
        return self.opposition

    def getMatchData(self):
        matchData = self.matchID + self.teamNumber + self.location + self.time + self.day + self.opposition
        return matchData
