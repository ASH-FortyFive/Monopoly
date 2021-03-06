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
import random

#OtherScripts
import MonopolySimInit 
from MonopolySimInit import Space

import MonopolyAgent 
from MonopolyAgent import Player



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

## Logger ##
def addToLog(_txt):
    #print(_txt)
    log = open(os.path.join(scriptpath,"MonopolyLog.txt"), "a")
    log.write(str(_txt))
    log.write('\n')
    log.close()

## SECTION ONE CHECKING VALUES ##
# The functions here are used to check if later moves are valid/possible
#Checks how many properties in a given set a player has

def hasHowManyOfSet(_player, _colourSet):
    amountOfSet = 0
    for ownedProperty in _player.ownedProperties:
        if ownedProperty.colourSet == _colourSet:
            amountOfSet += 1
    return amountOfSet

# Checks if a Player has a full set of a given property
def hasFullSet(_player, _colourSet):
    amountOfSet = 0
    amountOfSet = hasHowManyOfSet(_player, _colourSet)
    #Returns true when part of a small set
    if((_colourSet == 0 or _colourSet == 7) and amountOfSet == 2):
        return True
    #Returns true when part of a large set
    elif((_colourSet != 0 and _colourSet != 7 and _colourSet != 8 and _colourSet != 9 and _colourSet != 10) and amountOfSet == 3):
        return True
    else:
        return False

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

## SECTION TWO EFFECTING PLAYER ##
# The functions here effect he player in various ways

#Handels Paying For Things ##INCOMPLETE
def payFor(_player, _amount, _target):
    if(_player.money >= _amount):
        _player.money -= _amount
    else:
        #Complicated Code that needs to be added to acount for selling things
        _player.money -= _amount
    if(_target != None):
        _target.money += _amount
        addToLog("\t("+_player.id+") Paid "+str(_amount) + " to " +_target.id)
    else:
        addToLog("\t("+_player.id+") Paid "+str(_amount) + " to the Bank")

#Buying and Selling Properties is always done with these functions
#This is done in part so that updating the list of owned sets remains accurate
def buyProperty(_player, _space, _cost):
    payFor(_player, _cost, None)
    _space.owner = _player
    _player.ownedProperties.append(_space)
    if(hasFullSet(_player, _space.colourSet)):
        #print(_player.id + " got set " + str(_space.colourSet))
        _player.ownedSets.append(_space.colourSet)
        _player.ownedSets.sort()

    addToLog("\t("+_player.id+") bought " + _space.id +" for " +str(_cost)+ "("+str(_player.money) +" left)") 


def sellProperty(_player, _space, _cost):
    payFor(_player, _space.cost, None)
    _space.owner = None
    _player.ownedProperties.remove(_space)
    _player.ownedSets.remove(_space.colourSet)
    _player.ownedSets.sort()

    addToLog("\t("+_player.id+") sold " + _space.id +" for " +str(_cost)+ "("+str(_player.money) +" now)") 

def goToJail(_player):

    addToLog("\t("+_player.id+") Went to Jail") 

    _player.inJail = True
    _player.turnsInJail = 0
    _player.position = 10

#Moves player from A to B
def movePlayer(_player, _target):
    if(_target <= _player.position):
        #If the Target is before current position, you must have passed go
        _player.money += 200
    
    addToLog("\t("+_player.id+") is on " + Spaces[_target].id) 


    _player.position = _target

## SECTION 3 DURING A TURN ##
# Everything that happens during a turn, this is where the Agent script is called

#Functions to do very basic things
def roll2d6():
    rollList = [random.randint(1,6),random.randint(1,6)]
    rollList.append(rollList[0] + rollList[1])
    return rollList

#Handels Landing on Special Spaces
def OnSpecial(_player, _space):
    if(_space.id == "Income Tax"):
        payFor(_player, 200, None)
    elif(_space.id == "Chance"):
        chanceCard(_player)
    elif(_space.id == "Community"):
        communityCard(_player)
    elif(_space.id == "Go To Jail"):
        goToJail(_player)
    elif(_space.id == "Super Tax"):
        payFor(_player, 100, None)
    #All spaces that 'do' nothing
    elif(_space.id == "Free Parking" or "Go" or "Jail"):
        1 == 1
        #Does Nothing
    else:
        print("Error, invalid non-property space with the label " + str(_space.id))

#Community cards INCOMPLETE
def communityCard(_player):
    1 == 1

#Chance cards INCOMPLETE
def chanceCard(_player):
    1 == 1
    
#When a player chooses not to buy the property they landed on
def auctionProperty(_player, _space):
    addToLog("\t"+_space.id +" is up for auction!") 
    auctionOrder = []
    auctionIndex = Players.index(_player)

    OrderString = "\t\tAuction Order is: "
    #Makes the auction ordered list of players
    for i in range(len(Players)):
        auctionOrder.append(Players[(auctionIndex + i) % len(Players)])
        # Test String
        OrderString = OrderString + Players[(auctionIndex + i) % len(Players)].id + ", "
    
    addToLog(OrderString) 
        
    currentBid = 0
    bid = 0
    highestBidder = auctionOrder[len(Players)-1]

    Bidding = True

    while(Bidding):
        for player in auctionOrder:
            bid = player.BidOnProperty(_space,currentBid)
            if(highestBidder == player):
                Bidding = False
                break
            if(bid > (currentBid + 1)): 
                addToLog("\t\t"+player.id +" bids " + str(bid))
                highestBidder = player
                currentBid = bid

    addToLog("\t\t"+highestBidder.id +" won the auction at " + str(currentBid)) 


#Handels Landing on Property
def OnProperty(_player, _space, _diceRoll):
    if _space.owner == None:
        # Checks with player "agent" if they want to buy the property
        if(_player.BuyProperties(_space, _space.cost)):
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
                amountOwed = 4 * _diceRoll
            elif amountOfUtilites == 2:
                amountOwed = 10 * _diceRoll
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
        

#Handels "turns" where the player is not in jail, can happen more than once a turn due to doubles
def normalTurn(_player, _movement, _diceRoll):
     #Checks if Go was passed by seeing if where the player will be is a lower number than where it was
    targetPosition = (_player.position + _movement) % 40
    movePlayer(_player, targetPosition)

    _player.inJail = False
    _player.turnsInJail = 0

    space = Spaces[_player.position]
   

    # ALL DECSIONS FOLLOW THIS POINT##
    if space.isProperty:
        OnProperty(_player, space, _diceRoll)
    else:
        OnSpecial(_player, space)

    #Checks if they have sets so they can start building houses
    if(len(_player.ownedSets) != 0):
        for fullSet in _player.ownedSets:
            Buying = True
            while Buying:
                Buying = False
                for position in MonopolySimInit.PropertiesInSet[fullSet]:
                    nextProperty = Spaces[position]
                    if(nextProperty.numberOfHouses < maxHouseLevel(fullSet)):
                        if(_player.BuyHouses(nextProperty) == True):
                            addToLog("\t("+_player.id+") Bought a house on " + nextProperty.id +" (part of set "+str(fullSet) +")")
                            Buying = True
                            payFor(_player, nextProperty.costOfHouse, None)
                            nextProperty.numberOfHouses = nextProperty.numberOfHouses + 1
                            

#Main Action
def TakeTurn(_player):
    addToLog(_player.id + ": ")

    #Rolls dice, for moving or leaving jail
    DiceRoll = roll2d6()
    lastDiceRoll = 0

    addToLog("\t("+_player.id+") First  roll: " + str(DiceRoll[0])+" + "+ str(DiceRoll[1]))

    if(_player.inJail and _player.turnsInJail != 3):
        if DiceRoll[0] != DiceRoll[1]:
            #print(_player.id + " has been in Jail " +str(_player.turnsInJail) + " turns" )
            _player.turnsInJail += 1
            return
        #print(_player.id + " escaped jail with " + str(DiceRoll[0])+ " and "+str(DiceRoll[1]))
    elif(_player.turnsInJail == 3):
        if DiceRoll[0] != DiceRoll[1]:
            #print(_player.id + " is out of Jail")
            payFor(_player, 50, None)
    
    lastDiceRoll = DiceRoll[2]
    normalTurn(_player, DiceRoll[2],lastDiceRoll)
    if DiceRoll[0] == DiceRoll[1] and _player.inJail == False:
        DiceRoll = roll2d6()
        lastDiceRoll = DiceRoll[2]
        addToLog("\t("+_player.id+") Second  roll: " + str(DiceRoll[0])+" + "+ str(DiceRoll[1]))
        normalTurn(_player, DiceRoll[2],lastDiceRoll)

        if DiceRoll[0] == DiceRoll[1]:
            DiceRoll = roll2d6()
            lastDiceRoll = DiceRoll[2]
            addToLog("\t("+_player.id+") Third  roll: " + str(DiceRoll[0])+" + "+ str(DiceRoll[1]))
            normalTurn(_player, DiceRoll[2],lastDiceRoll)

            if DiceRoll[0] == DiceRoll[1]:
                addToLog("\t("+_player.id+") Rolled three doubles!")
                goToJail(_player)
                return

## SECTION FOUR CORE GAME LOOP ##
# The main game loop, and some debug functions
    
 #Main Loop   
def game():
    #Clear Log
    if os.path.exists(os.path.join(scriptpath,"MonopolyLog.txt")):
        os.remove(os.path.join(scriptpath,"MonopolyLog.txt"))

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

                    addToLog(str(Players[playerToCheck].id + " is Bankrupt!"))
                    
                    Players.remove(Players[playerToCheck])
                playerToCheck += 1

            # Monopoly ends when the second player is bankrupt
            if len(Players) == 1:
                addToLog(str(Players[0].id) + " won in " +str(TurnNumber)+ " turns")

                GameOver = True

        if TurnNumber == 500:
            #For Dedug
            addToLog('Game was a tie, remaining players were:')

            Players.sort(key=operator.attrgetter('money'))
            Players.reverse()
            for player in Players:
                addToLog((player.id + ': ' + str(player.money)))

                GameOver = True

        TurnNumber += 1

        
game()


        
    


