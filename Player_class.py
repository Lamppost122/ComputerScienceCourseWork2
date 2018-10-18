

"""

Player class

This is the tool set for creating a new player instance

It also contains the validation for creating a new player instance

Note:

    Need to add validation

"""

import re,datetime,io,sys,os.path,os


class player():
    def __init__(self,playerID,firstName,lastName,Email,phoneNumber,Address,Postcode,dateOfBirth,dateOfJoining):
        self.playerID = self.getPlayerID()
        self.firstName = firstName
        self.lastName = lastName
        self.Email = Email
        self.phoneNumber = phoneNumber
        self.Address = Address
        self.Postcode = Postcode
        self.dateOfBirth = dateOfBirth
        self.dateOfJoining = self.getDateOfJoining()

    def getPlayerID(self):
        File = open("playerDatabase.txt","r")
        data = File.readlines()


        if len(data) != 0 :
            data =  str(data[-1])
            playerID=int(data[0:5])+1
            playerID = "{:05d}".format(playerID)
            playerID = str(playerID)
        else:
            playerID = "00001"

        return playerID


    def getFirstName(self,firstName):

        if len(firstName) > 30 :
            self.getFirstName()
        firstName = "{:<30}".format(firstName)
        firstName.lower()
        return firstName

    def getLastName(self,lastName):

        if len(lastName) > 30 :
            playerDatabase.getLastName()
        lastName = "{:<30}".format(lastName)
        lastName.lower()
        return lastName

    def getEmail(self,Email):

        if len(Email) > 30:
            self.getEmail()
##        if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", self.Email) != False:
##            self.getEmail()
        Email = "{:<30}".format(Email)
        return Email

    def getPhoneNumber(self,phoneNumber):
##        if len(self.PhoneNumber) != 11:
##            self.getPhoneNumber()
##        if self.PhoneNumber.isdigit() == False:
##            self.getPhoneNumber()
        return phoneNumber

    def getAddress(self,Address):

        if len(Address) > 30:
            self.getAddress()
        Address = "{:<30}".format(Address)
        return Address

    def getPostcode(self,Postcode):

##        if re.match("^(([gG][iI][rR] {0,}0[aA]{2})|((([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y]?[0-9][0-9]?)|(([a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y]))) {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2}))$)",Postcode) == False:
##            playerDatabase.getPostcode()
        Postcode.replace(" ","")
        return Postcode

    def getDateOfBirth(self, dateOfBirth):

##        try:
##            datetime.datetime.strptime(inputDob, '%d/%m/%Y')
##        except ValueError:
##            playerDatabase.getDateOfBirth()
        return dateOfBirth

    def getDateOfJoining(self):
        DateOfJoining = str(datetime.datetime.now())
        return DateOfJoining


    def getPlayerData(self):
        playerData = self.playerID + self.firstName + self.lastName + self.Email+self.phoneNumber+self.Address+self.Postcode+self.dateOfBirth+self.dateOfJoining
        return playerData

