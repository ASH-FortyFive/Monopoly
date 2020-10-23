#Runs Monopoly Many Many Times
i = 0
while(i < 10000):
    f = open("MonopolyLog.txt", "a")
    f.write('\n')
    f.write('\n')
    f.write(str('Game: ' +str(i + 1)))
    f.close()
    
    print('Game: ' +str(i + 1))
    execfile('MonopolySim.py')

    i += 1
