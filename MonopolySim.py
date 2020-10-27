 #Auto Monopoly
#A Monopoly simulation by ASH
#This Part is the "main script" that references all others

#Follows Rules Found on the following URL:
#https://system.na2.netsuite.com/core/media/media.nl?id=488686&c=902231&h=9fc37d8b226fe536bbfe&_xt=.pdf


#Imports
import sys
import os
import os.path

import operator
import MonopolySimInit 
from MonopolySimInit import Space
from MonopolySimInit import Player
import random

#Functions to do very basic things
def roll2d6():
    rollList = [random.randint(1,6),random.randint(1,6)]
    rollList.append(rollList[0] + rollList[1])
    return rollList

##TEMPORARY## 
#Information for "Bots"
minimumSafteyNet = 250
#Knobs to fiddle with
completeSetMulti = 3
completeSetPercent = .5

possibleSetMulti = 1.5
possibleSetPercent = .2

emptySetPercent = .1


GameOver = False

#Sets inital Values
initalMoney = 1500
RemainingHouses = 32
RemainingHotels = 12
NumberOfPlayers = 3


#All the Data to do with individual Properties
#Attaches Set Colors to Numbers, for clarity
SetColour = MonopolySimInit.SetColour


#Clears players and Spaces
Spaces = [] 
Players = []



scriptpath = os.path.dirname(__file__)
#Reads CSV file for information about the Game
#First it Reads the Token Names File
TokenNames = MonopolySimInit.ReadTokens(os.path.join(scriptpath, 'MonopolyData - Tokens.txt'))
#Then the Spaces File
Spaces = MonopolySimInit.ReadSpaces(os.path.join(scriptpath,'MonopolyData - Spaces.txt'))
#Initlisizes Players
Players = MonopolySimInit.genPlayers(NumberOfPlayers, TokenNames, initalMoney)



#Sets / Resets all values that can change
def InitGame():
    GameOver = False

    #Sets inital Values
    initalMoney = 1500
    RemainingHouses = 32
    RemainingHotels = 12
    NumberOfPlayers = 3


    #All the Data to do with individual Properties
    #Attaches Set Colors to Numbers, for clarity
    SetColour = MonopolySimInit.SetColour


    #Clears players and Spaces
    Spaces = [] 
    Players = []

    #Reads CSV file for information about the Game
    #First it Reads the Token Names File
    TokenNames = MonopolySimInit.ReadTokens('MonopolyData - Tokens.txt')
    #Then the Spaces File
    Spaces = MonopolySimInit.ReadSpaces('MonopolyData - Spaces.txt')
    #Initlisizes Players
    Players = MonopolySimInit.genPlayers(NumberOfPlayers, TokenNames, initalMoney)

#Handels Landing on Special Spaces
#Not a very elegant solution
def OnSpecial(_player, _space):
    if(_space.id == "Income Tax"):
        payFor(_player, 200, False)
    elif(_space.id == "Chance"):
        #print(str(_player.id) + " is drawing a chance card")
        1 == 1
    elif(_space.id == "Community"):
        #print(str(_player.id) + " is drawing a Community card")
        1 == 1
    elif(_space.id == "Go To Jail"):
        goToJail(_player)
    elif(_space.id == "Super Tax"):
        payFor(_player, 100, False)
    #All spaces that 'do' nothing
    elif(_space.id == "Free Parking" or "Go" or "Jail"):
        1 == 1
    else:
        print("Error, invalid non-property space with the label " + str(_space.id))



#Checks if a Player has a full set of a given property
def hasHowManyOfSet(_player, _colourSet):
    amountOfSet = 0
    for ownedProperty in _player.ownedProperties:
        #print(str(ownedProperty.colourSet) +" "+ str(_colourSet) + " " + str(ownedProperty.colourSet == _colourSet))
        if ownedProperty.colourSet == _colourSet:
            #print(_player.id + " owns " + ownedProperty.id)
            amountOfSet += 1
    
    #print((_player.id + " has " + str(amountOfSet) + " of colour set "+ str(_colourSet)))
    
    return amountOfSet

def hasFullSet(_player, _colourSet):
    amountOfSet = 0
    amountOfSet = hasHowManyOfSet(_player, _colourSet)
    if((_colourSet == 0 or _colourSet == 7) and amountOfSet == 2):
        return True
    elif((_colourSet != 0 and _colourSet != 7 and _colourSet != 8 and _colourSet != 9 and _colourSet != 10) and amountOfSet == 3):
        return True
    else:
        return False
    
#Handels Paying For Thingst
def payFor(_player, _amount, _target):
    if(_player.money >= _amount):
        _player.money -= _amount
    else:
        #Complicated Code that needs to be added
        _player.money -= _amount
    if((type(_target).__name__) == "instance"):
        _target.money += _amount


#Buying and Selling Properties is always done with these functions
#This is done in part so that updating the list of owned sets remains accurate
def buyProperty(_player, _space, _cost):
    ##DEBUG
    #print(_space.id + " bought by " + _player.id)
    #for play in Players:
    #    print(play.id + " would "+ str(propertyValue(play, _space))+ ", in set " + str(hasHowManyOfSet(play, _space.colourSet)) + ", bling "+ str(play.money))
    ##DEBUG
    payFor(_player, _cost, False)
    _space.owner = _player
    _player.ownedProperties.append(_space)
    if(hasFullSet(_player, _space.colourSet)):
        #print(_player.id + " got set " + str(_space.colourSet))
        _player.ownedSets.append(_space.colourSet)
        _player.ownedSets.sort()

def sellProperty(_player, _space, _cost):
    payFor(_player, _space.cost, False)
    _space.owner = None
    _player.ownedProperties.remove(_space)
    _player.ownedSets.remove(_space.colourSet)
    _player.ownedSets.sort()

#When a property is not purchased
def auctionProperty(_player, _space):
    auctionOrder = []
    auctionIndex = Players.index(_player)
    previousBid = -1
    currentBid = 0

    #Makes the auction ordered list of players
    i = 0
    while i < (len(Players)):
        auctionOrder.append(Players[(auctionIndex + i) % len(Players)])
        i += 1
    currentBidder = auctionOrder[0]
    while(currentBid != previousBid):
        previousBid = currentBid
        for bidder in auctionOrder:
            if(propertyValue(bidder, _space) > currentBid):
                currentBid += 10
                currentBidder = bidder

    #print(bidder.id + ' bought ' + _space.id + ' for ' + str(currentBid))

#This is how much a basic "AI" player values a property used in auctions and maybe trades
def propertyValue(_player, _space):
    possibleValue = 0
    value = _space.cost
    colourSet = _space.colourSet
    amountOfSet = hasHowManyOfSet(_player, colourSet)

    #The First if statement checks if this property would complete a set
    if(((colourSet == 0 or 7 or 9) and (amountOfSet == 1)) \
    or ((colourSet != 0 or 7 or 9 or 8) and (amountOfSet == 2)) \
    or ((colourSet == 8) and(amountOfSet == 3 or 2))):
        #The value here is arbirarty and can be changed
        #Current Logic is as follow, sets are really good and the AI will do anything short of bankrupting itself to buy them
        if(((_space.cost  * completeSetMulti) + (_player.money * completeSetPercent)) < (_player.money- minimumSafteyNet)):
            #print("1")
            value = ((_space.cost  * completeSetMulti) + (_player.money * completeSetPercent))
        elif(((_space.cost  * completeSetMulti)) < (_player.money- minimumSafteyNet)):
            #print("2")
            value = ((_space.cost  * completeSetMulti))
        elif(((_space.cost + (_player.money * completeSetPercent)) < (_player.money- minimumSafteyNet))):
            #print("3")
            value = ((_space.cost + (_player.money * completeSetPercent)))
        elif(((_space.cost + (_player.money * possibleSetPercent)) < (_player.money- minimumSafteyNet))):
            #print("4")
            value = ((_space.cost + (_player.money * possibleSetPercent)))
    #This shows that they have one of the set
    elif(amountOfSet == 1):
        #The value here is arbirarty and can be changed
        #Current Logic is as follow, sets are really good and the AI will do anything short of bankrupting itself to buy them
        if(((_space.cost  * possibleSetMulti ) + (_player.money * possibleSetPercent )) < (_player.money- minimumSafteyNet)):
            #print("5")
            value = ((_space.cost  * possibleSetMulti ) + (_player.money * possibleSetPercent ))
        elif(((_space.cost  * possibleSetMulti )) < (_player.money- minimumSafteyNet)):
            #print("6")
            value = ((_space.cost  * possibleSetMulti ))
        elif(((_space.cost + (_player.money * possibleSetPercent)) < (_player.money- minimumSafteyNet))):
            #print("7")
            value = ((_space.cost + (_player.money * possibleSetPercent)))
    else:
        if(((_space.cost + (_player.money * emptySetPercent)) < (_player.money- minimumSafteyNet))):
            #print("8")
            value = ((_space.cost + (_player.money * emptySetPercent)))
        else:
            #print("9")
            value = _player.money- minimumSafteyNet
    return value   

#Handels Landing on Property
def OnProperty(_player, _space):
    #This Part is A temprary algorythm, eventually to be replaced
    if _space.owner == None:
        if(_player.money >= _space.cost):
            buyProperty(_player, _space, _space.cost)
        else:
            auctionProperty(_player, _space)
    elif _space.owner != _player:
        #Rail
        if _space.colourSet == 8:
            payFor(_player, _space.rentList[hasHowManyOfSet(_space.owner, _space.colourSet) - 1], _space.owner)
        #Utility
        elif _space.colourSet == 9:
            amountOfUtilites = hasHowManyOfSet(_space.owner, _space.colourSet)
            if amountOfUtilites == 1:
                amountOwed = 4 * lastDiceRoll
            elif amountOfUtilites == 2:
                amountOwed = 10 * lastDiceRoll
            else:
                print("Too many utilities")
            payFor(_player, amountOwed, _space.owner)
        else:
            if _space.numberOfHouses == 0:
                if(_space.colourSet in _space.owner.ownedSets):
                    payFor(_player, _space.rentList[0] * 2, _space.owner)
                else:
                    payFor(_player, _space.rentList[0], _space.owner)
            else:
                payFor(_player, _space.rentList[_space.numberOfHouses], _space.owner)
        
def goToJail(_player):
    #print(_player.id + " went to Jail")
    _player.inJail = True
    _player.turnsInJail = 0
    _player.position = 10

RemainingHouses = 32
RemainingHotels = 12

#Temporary Function that lets the Bots build houses
def buyHouses(_player):
    global RemainingHouses
    global RemainingHotels
    #Inverts list as to buy "better" houses first
    ownedSets = (_player.ownedSets)
    ownedSets.reverse()
    
    for ownedSet in ownedSets:
        posOfPropsInSet = MonopolySimInit.PropertiesInSet[ownedSet]
        posOfPropsInSet.reverse()
        for position in posOfPropsInSet:
            space = Spaces[position]
            maxLevel = maxHouseLevel(ownedSet)
            if(((_player.money - 200) > space.costOfHouse)\
               and space.numberOfHouses < maxLevel):
                #Deals with limited number of houses and hotels
                if(maxLevel == 5 and RemainingHotels != 0):
                    RemainingHouses += 4
                    RemainingHotels -= 1
                    space.numberOfHouses += 1
                elif(RemainingHouses != 0):
                    RemainingHouses -= 1
                    space.numberOfHouses += 1


#Returns the current max number of houses on a property
def maxHouseLevel(_set):
    levels = []
    for position in MonopolySimInit.PropertiesInSet[_set]:
        levels.append(Spaces[position].numberOfHouses)

    #Checks if all values are the same or not
    if(len(levels) == 2):
        if(levels[0] == levels[1]):
            if (max(levels) == 5):
                return 5
            else:
                return max(levels) + 1
    elif(len(levels) == 3):
        if(levels[0] == levels[1]) and (levels[1] == levels[2]):
            if (max(levels) == 5):
                return 5
            else:
                return max(levels) + 1
    else:
        print('Set with too many properties')
    
    return max(levels)
    
#Handels "turns" where the player is not in jail, can happen more than once a turn due to doubles
def normalTurn(_player, _movement):
     #Checks if Go was passed by seeing if where the player will be is a lower number than where it was
    targetPosition = (_player.position + _movement) % 40
    if(targetPosition <= _player.position):
        #If the Target is before current position, you must have passed go
        _player.money += 200
    _player.position = (_player.position + _movement) % 40

    _player.inJail = False
    _player.turnsInJail = 0

    space = Spaces[_player.position]
   
    if space.isProperty:
        OnProperty(_player, space)
    else:
        OnSpecial(_player, space)

    #Checks if they have sets so they can start building houses
    setsAlreadyChecked = []
    if(len(_player.ownedSets) != 0):
        buyHouses(_player)

lastDiceRoll = 0
#Main Action
def TakeTurn(_player):
    
    #Rolls dice, for moving or leaving jail
    DiceRoll = roll2d6()
    lastDiceRoll = 0

    if(_player.inJail and _player.turnsInJail != 3):
        if DiceRoll[0] != DiceRoll[1]:
            #print(_player.id + " has been in Jail " +str(_player.turnsInJail) + " turns" )
            _player.turnsInJail += 1
            return
        #print(_player.id + " escaped jail with " + str(DiceRoll[0])+ " and "+str(DiceRoll[1]))
    elif(_player.turnsInJail == 3):
        if DiceRoll[0] != DiceRoll[1]:
            #print(_player.id + " is out of Jail")
            payFor(_player, 50, False)
    
    lastDiceRoll = DiceRoll[2]
    normalTurn(_player, DiceRoll[2])
    if DiceRoll[0] == DiceRoll[1] and _player.inJail == False:
        DiceRoll = roll2d6()
        lastDiceRoll = DiceRoll[2]
        normalTurn(_player, DiceRoll[2])
        if DiceRoll[0] == DiceRoll[1]:
            DiceRoll = roll2d6()
            lastDiceRoll = DiceRoll[2]
            normalTurn(_player, DiceRoll[2])
            if DiceRoll[0] == DiceRoll[1]:
                goToJail(_player)
                return

def addToLog(_txt):
    f = open(os.path.join(scriptpath,"MonopolyLog.txt"), "a")
    f.write('\n')
    f.write(str(_txt))
    f.close()
    
 #Main Loop   
def game():

    ##For Keeping Logs
    TurnNumber = 1
    
    global GameOver
    while GameOver == False:
        #Gives each player a turn
        for player in Players:
            TakeTurn(player)

            #Checks if game is over after every round of play    
            playerToCheck = 0
            while playerToCheck < len(Players):
                if Players[playerToCheck].money <= 0:
                    #print(Players[playerToCheck].id + " is Bankrupt!")
                    Players.remove(Players[playerToCheck])
                playerToCheck += 1
            if len(Players) == 1:
                #print(str(Players[0].id) + " won in " +str(TurnNumber)+ " turns")
                addToLog(str(Players[0].id) + " won in " +str(TurnNumber)+ " turns")
                GameOver = True

        if TurnNumber == 1000:
            #print('Game was a tie, remaining players were:')
            addToLog('Game was a tie, remaining players were:')
            Players.sort(key=operator.attrgetter('money'))
            Players.reverse()
            for player in Players:
                addToLog((player.id + ': ' + str(player.money)))
                #print(player.id + ': ' + str(player.money))
                GameOver = True

        TurnNumber += 1

        

GameOver = False
game()


        
    


