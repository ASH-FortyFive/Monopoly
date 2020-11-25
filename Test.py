test = ["Dog","Bird","Cat","Fish"]

for x in test:
    if(len(x) == 4):
        test.remove(x)
    print(x +" has length " + str(len(x)))
    
    