import random
import matplotlib.pyplot as plt
import json
class InsideTile:
    def __init__(self, name, payout, colour):
        self.name = name
        self.payout = payout
        self.colour = colour

class OutsideTile:
    def __init__(self, name, payout, cover):
        self.name = name
        self.payout = payout
        self.cover = cover #Where cover = Array of InsideTile names

class Table:
    def __init__(self, name, inside, outside):
        self.name = name
        self.inside = inside
        self.outside = outside
    


class payoutTable:
    def __init__(self, largestLoss, currentCash, numberOfSpins):
        self.largestLoss = largestLoss
        self.currentCash = currentCash
        self.numberOfSpins = numberOfSpins
    
    def printer(self):
        print("Current Cash: " + str(self.currentCash) + " | Largest Loss: " + str(self.largestLoss) + " | Number of Spins: " + str(self.numberOfSpins))

redTiles = []#[1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
blackTiles = []#[2,4,6,8,10,11,15,17,20,22,24,26,28,29,31,33,35]

settingsFile = ""

def buildTable():
    arrayOfInsideTiles = []
    for i in range(1,36):
        if i in redTiles:
            colour = 'red'
        else:
            colour = 'black'
        arrayOfInsideTiles.append(InsideTile(i,35,colour))
    
    arrayOfInsideTiles.append(InsideTile(0,35,'green'))
    return Table('table',arrayOfInsideTiles,[])



def checkPayout(bet, spin, betAmount):
    if (bet == 0 and (spin in redTiles)):
        return (betAmount*2)
    
    if (bet == 1 and (spin in blackTiles)):
        return (betAmount*2)

    return -1*betAmount

def printer():
    print("Print")
    #print("Colour: " + str(betColour) + " | Amount: " + str(bet) + " | Spin Number: " + str(spin) + " | Spin Colour (0 = Black, 1 = Red): " + str(int(spin in redTiles)))
    #print("Current Cash: " + str(currentMoney) + " | Current Loss: " + str(loss) + " | Payout of Last Spin: " + str(payout))

def printStatus(currentMoney, loss, payout):
    print("Current Cash: " + str(currentMoney))


def compare(tables, startingCash):
    highestWinrate = 0
    lowestWinrate = 1000
    arrayOfCash = []
    numberOfTables = len(tables)
    bobe = 0

    for t in tables:
        if t.currentCash > highestWinrate:
            highestWinrate = t.currentCash
        if t.currentCash < lowestWinrate:
            lowestWinrate = t.currentCash
        if t.currentCash <= startingCash:
            bobe += 1
        arrayOfCash.append(t.currentCash)

    print("Number of Tables: " + str(numberOfTables) + " | # of Tables Even or Below: " + str(bobe))
    print("Highest Win Rate: " + str(highestWinrate) + " | Lowest Win Rate: " + str(lowestWinrate))
    plt.style.use('Solarize_Light2')
    plt.plot(arrayOfCash)
    plt.show()


def loadSettings(settingsFile):
    global redTiles
    global blackTiles
    redTiles = settingsFile['redTiles']
    blackTiles = settingsFile['blackTiles']


def getSettings(settingsFile):
    return json.load(open(settingsFile))


def main():
    settingsFile = getSettings('settings.json')
    print(settingsFile)
    loadSettings(settingsFile)

    tables = []
    iterations = settingsFile['numberOfIterations']
    for j in range(iterations):
        numberOfSpins = settingsFile['maxNumberOfSpins']
        currentMoney = settingsFile['startingAmount']
        loss = 0
        largestLoss = 0
        betColour = 0
        maxLoss = settingsFile['maxLossBeforeBail']
        spinCount = 0
        for i in range(numberOfSpins):
            spinCount += 1
            if(currentMoney <= 0 or loss > maxLoss):
                break

            spin = random.randrange(0, 36)
            if(loss == 0):
                bet = 5
            else:
                if(loss > largestLoss):
                    largestLoss = loss
                bet = loss
            
            payout = checkPayout(betColour,spin,bet)
            currentMoney += payout
            if (payout < 0):
                loss += (-1*payout)
            else:
                loss = 0
        tables.append(payoutTable(largestLoss,currentMoney,spinCount))
    
    compare(tables, 500)

        
            






if __name__ == "__main__":
    main()