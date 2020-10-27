#Runs Monopoly Many Many Times
import os.path, sys

from MonopolySim import game

scriptpath = os.path.dirname(__file__)

i = 0
while(i < 100):
    f = open(os.path.join(scriptpath,"MonopolyLog.txt"), "a")
    f.write('\n')
    f.write('\n')
    f.write(str('Game: ' +str(i + 1)))
    f.close()
    
    print('Game: ' +str(i + 1))
    exec(open((os.path.join(scriptpath,'MonopolySim.py')).read()))

    i += 1
