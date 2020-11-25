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

    def BuyProperties(self, _space,_price):
        if(_price*3 < self.money):
            return True
        return False
    def BidOnProperty(self, _space,_price):
        if(_price*3 < self.money):
            return int( _price + 5 + self.money * .05)
        return 0
    def BuyHouses(self, _space):
        if(_space.costOfHouse*2 < self.money):
            return True
        return False

def Sell():
    1==1
