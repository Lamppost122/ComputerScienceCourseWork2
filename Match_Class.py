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
        self.matchID = sum(1 for line in open("matchFile.txt")) + 1
        self.matchID = "{:05d}".format(self.matchID)
        self.matchID = str(self.matchID)
        return self.matchID

    def getTeamNumber(self):
        self.teamNumber = raw_input("What team is playing in the match?")
        self.teamNumber = "{:03d}".format(int(self.teamNumber))
        self.teamNumber = str(self.teamNumber)
        return self.teamNumber

    def getLocation(self):
        self.location = raw_input("Where is the match being played ?")
        if len(self.location) > 30 :
            self.getLocation()
        self.location = "{:<30}".format(self.location)
        self.location.lower()
        return self.location

    def getTime(self):
        self.time = raw_input("What time is the match being played")
        return self.time

    def getDay(self):
        self.day = raw_input("What day is the match ? ")
        return self.day

    def getOpposition(self):
        self.opposition = raw_input("Who is playing against ?")
        if len(self.opposition) > 30 :
            self.getOpposition()
        self.opposition = "{:<30}".format(self.opposition).lower()
        return self.opposition

    def getMatchData(self):
        matchData = self.matchID + self.teamNumber + self.location + self.time + self.day + self.opposition
        return matchData
