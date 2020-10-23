 #Auto Monopoly
#A Monopoly simulation by ASH
#This Part feature all functions that are run once when initlizing the gamed

#Follows Rules Found on the following URL:
#https://system.na2.netsuite.com/core/media/media.nl?id=488686&c=902231&h=9fc37d8b226fe536bbfe&_xt=.pdf

#Imports
import csv
import random

#All the Data to do with individual Properties
#Attaches Set Colors to Numbers, for clarity
SetColour = {
        "Brown": 0,
        "LightBlue": 1,
        "Pink": 2,
        "Orange": 3,
        "Red": 4,
        "Yellow": 5,
        "Green": 6,
        "DarkBlue": 7,
        "Rail": 8,
        "Utilities": 9,
        "None": 10
    }

PropertiesInSet = {
    0: [1,3],
    1: [6,8,9],
    2: [11,13,14],
    3: [16,18,19],
    4: [21,23,24],
    5: [26,27,29],
    6: [31,32,34],
    7: [37,39]
    }
    

#Defines the Space class, which contains the data needed to create a "space" on the monopoly board
class Space:
    position = 0
    id = ""
    isProperty = False
    colourSet = 0
    cost = 0
    costOfHouse = 0
    #5 is a hotel
    numberOfHouses = 0
     #Rent ranging from Zero to Hotel, in order
    rentList = (0,1,2,3,4,5)
    owner = None
    def __init__(self, _Position, id, _IsProperty, _Set, _Cost, _CostOfHouse, _RentList,):
        self.id = id
        self.position = _Position
        self.isProperty = _IsProperty
        self.colourSet = _Set
        self.cost = _Cost
        self.costOfHouse = _CostOfHouse
        self.rentList = _RentList

#Defines the Player class, which contains the informatin needed about each player (PC and NPC)
class Player:
    money = 0
    ownedProperties = []
    ownedSets = []
    #Where they are on the board
    position = 0
    inJail = False
    turnsInJail = 0
    def __init__(self, _InitalMoney,id):
        self.position = 0
        self.money = _InitalMoney
        self.id = id
        self.ownedProperties = []
        self.ownedSets = []

#Reads a CSV to get player/token names
#Returns a list
def ReadTokens(_path):
    tokens = []
    with open(_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0
        for row in csv_reader:
            while i < len(row):
                tokens.append(row[i])
                i += 1
    return tokens

#Read a CSV to get information for spaces
#Returns a list
def ReadSpaces(_path):
    spaces = []
    with open(_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                if row[0] == 'Property':
                    tempRentList = [10,20,30,40,50,100]
                    rentPerHouse = 0
                    while rentPerHouse < len(tempRentList):
                        tempRentList[rentPerHouse] = int(row[5 + rentPerHouse])
                        rentPerHouse += 1
                    tempSpace = Space(line_count - 1, row[1], True, int(SetColour[row[2]]), int(row[3]), int(row[4]),tempRentList)
                    spaces.append(tempSpace)
                else:
                    tempSpace = Space(line_count - 1, row[1], False, 10, 0,0,[0,0,0,0,0,0])
                    spaces.append(tempSpace)
            line_count += 1
    return spaces

#Returns and Array with 'player' information
def genPlayers(_number, _tokenNames, _initalMoney):
    PlayerIndex = 0
    Players = []
    while PlayerIndex < _number:
        i = random.randint(0,len(_tokenNames)-1)
        Players.append( Player(_initalMoney, _tokenNames[i]) )
        _tokenNames.remove(_tokenNames[i])
        PlayerIndex += 1
    return Players
