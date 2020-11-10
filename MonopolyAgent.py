#Auto Monopoly
#A Monopoly simulation by ASH
#This Part is the 'agent' that plays monopoly, in my dreams this works with Machine Learning.

#Follows Rules Found on the following URL:
#https://system.na2.netsuite.com/core/media/media.nl?id=488686&c=902231&h=9fc37d8b226fe536bbfe&_xt=.pdf

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