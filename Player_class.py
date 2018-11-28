"""
Player class
This is the tool set for creating a new player instance
It also contains the validation for creating a new player instance
Note:
    Need to add validation
"""

import re,datetime,io,sys,os.path,os
from datetime import datetime, timedelta

class player():
    def __init__(self,playerID,firstName,lastName,Email,phoneNumber,Address,Postcode,dateOfBirth,dateOfJoining):
        self.playerID = playerID
        self.firstName = firstName
        self.lastName = lastName
        self.Email = Email
        self.phoneNumber = phoneNumber
        self.Address = Address
        self.Postcode = Postcode
        self.dateOfBirth = dateOfBirth
        self.dateOfJoining = dateOfJoining

    def getPlayerID(self):

##        data = self.readFile("playerDatabase.txt","r")
##
##        if len(data) != 0 :
##            data =  str(data[-1])
##            playerID=int(data[0:5])+1
##            playerID = "{:05d}".format(playerID)
##            playerID = str(playerID)
##        else:
##            playerID = "00001"
        playerID = "00001"
        return playerID


    def getFirstName(self,firstName):
        firstName.lower()
        return firstName

    def validFirstName(self,firstName):
        if len(firstName) <30:
            return True
        else:
            newFirstName = raw_input(firstName + " is not a valid first Name")
            self.validFirstName(newFirstName)



    def getLastName(self,lastName):
        lastName.lower()
        return lastName


    def validLastName(self,lastName):
        if len(lastName) <30:
            return True
        else:
            newLastName = raw_input(lastName +" is not a valid last Name")


    def getEmail(self,Email):
        return Email

    def validEmail(self,Email):
        if len(Email) > 7:
##            if re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", Email) != None:
                return True
        return "Email", Email, False

    def getPhoneNumber(self,phoneNumber):
        return phoneNumber

    def validPhoneNumber(self,phoneNumber):
        if phoneNumber.isdigit() == True:
            if phoneNumber[0] == "0" :
                if len(phoneNumber) == 11 :
                    return True
        return "Phone Number" , phoneNumber , False

    def getAddress(self,address):
        return address

    def validAddress(self,address):
        if len(address) < 30:
            return True
        return "Address",address,False

    def getPostcode(self,postcode):
        postcode.replace(" ","")
        return postcode

    def validPostcode(self,postcode):

##        if re.match("^(([gG][iI][rR] {0,}0[aA]{2})|((([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y]?[0-9][0-9]?)|(([a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y]))) {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2}))$)",postcode) == False:
            return True
##        return "Postcode", postcode , False

    def getDateOfBirth(self, dateOfBirth):
        return dateOfBirth

    def validDateOfBirth(self,dateOfBirth):
        try:
            datetime.strptime(dateOfBirth, '%d/%m/%Y')
        except ValueError:
            return "Date of Birth ",dateOfBirth,False
        if datetime.now() - timedelta(days=2000) > datetime.strptime(dateOfBirth, '%d/%m/%Y'):
            return True
        return "Date of Birth ",dateOfBirth, False

    def getDateOfJoining(self):
        DateOfJoining = str(datetime.now())
        return DateOfJoining


    def getPlayerData(self,playerID,firstName,lastName,Email,phoneNumber,Address,Postcode,dateOfBirth,dateOfJoining):
        playerData = [playerID,firstName,lastName,Email,phoneNumber,Address,Postcode,dateOfBirth,dateOfJoining]
        return playerData

    def validData(self,firstName,lastName,Email,phoneNumber,Address,Postcode,dateOfBirth):
        self.validFirstName(firstName)
        self.validLastName(lastName)
        self.validEmail(Email)
        self.validPhoneNumber(phoneNumber)
        self.validAddress(Address)
        self.validPostcode(Postcode)
        self.validDateOfBirth(dateOfBirth)




