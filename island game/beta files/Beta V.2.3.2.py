###Island game
###Beta V.3.5.1
###Changed how sections of ouputs are sent especially with time gaps
###Fixed "sell" function to give the right amount of money
###Made "sell" function add item back to market
###Added most comments onto code to be more readable

import time
import sys
import random


###functions to run at the start of the game/run
def new_game():
    newGame=input("would you like to play a new game?")
    if newGame=="no":
        pass
    elif newGame=="yes":
        backup=open("inventory of locations (backup).txt", "r")
        inventory_of_locations=open("inventory of locations.txt", "w")
        reset(inventory_of_locations, backup)
        inventory_of_locations.close()
        backup.close()
        #resets the locations inventories
        inventory=open("inventory.txt", "w")
        inventory.write("")
        inventory.close()
        #resets your inventory
        backup=open("items to buy (backup).txt", "r")
        market=open("items to buy.txt", "w")
        reset(market, backup)
        backup.close()
        market.close()
        #resets the markets inventory
    else:
        print("that wasn't a choce")
        while newGame!="yes" and newGame!="no":
            newGame=input("would you like a new game?")
    return newGame

def reset(file, backup):
    backupLines=backup.read().splitlines()
    for i in range(0, len(backupLines)):
        file.write(backupLines[i]+"\n")

def menu(locations, playerLocation, playerLocationNum):
    global inv_of_location
    print("welcome to the island lovely bunch of coconuts!")
    time.sleep(2)
    print("you are a citizen of the village in the south west section of the island")
    time.sleep(2)
    print("this is a layout of the island:")
    print()
    time.sleep(1)
    for i in range(0, 9):
        if (i+1)%3==0:
            print(locations[i]+",")
        else:
            print(locations[i]+", ", end="")
    print()
    time.sleep(2)
    print("you can go to any adjacent tile")
    time.sleep(1)
    print("except from the beach to the windmill (and vice versa)\n or the village to the cliffs (and vice versa)")
    time.sleep(2)
    inv_of_location=whatsHere(playerLocation, playerLocationNum)
    firstChoice=input("from the village, what would you like to do?")
    return firstChoice#prints the welcome messages and initiates your first choice



###functions to run thoughtout the game to find infomation e.g. read from files
def read_locations():
    readLocations=open("island game locations.txt", "r")
    locations=readLocations.read().splitlines()
    return locations#will return a list of all locations in the game

def locationNumFunc(location):
    if location=="mine":
        return 1
    elif location=="cliffs":
        return 3
    elif location=="town":
        return 4
    elif location=="windmill":
        return 5
    elif location=="village":
        return 6
    elif location=="forest":
        return 7
    elif location=="beach":
        return 8
    else:
        return -2
    #will return a number corresponding to the location asked
    #or -2 if the location is one you cannot go to or doesn't exist

def read_inventory():
    readInventory=open("inventory.txt", "r")
    inventory=readInventory.read().splitlines()
    return inventory#reads your inventory and returns it as a list

def create_dictionary():
    global dictionary
    inv_of_everywhere=open("inventory of locations.txt", "r")
    inv_of_everywhereSplit=inv_of_everywhere.read().splitlines()
    inv_of_everywhere.close()
    for i in range(0, len(inv_of_everywhereSplit)):
        for j in range(0, len(inv_of_everywhereSplit[i].split(" , "))):
            dictionary[i].append(inv_of_everywhereSplit[i].split(" , ")[j])
            #will read all locations inventories
            #and put them into a dictionary

def writeAllFromInv(dictionary):
    doc=open("inventory of locations.txt", "w")
    for i in range(0, len(dictionary)):
        for j in range(0, len(dictionary[i])):
            doc.write(dictionary[i][j])
            if j!=len(dictionary[i])-1:
                doc.write(" , ")
        doc.write("\n")
        dictionary[i]=""
    doc.close()#writes the dictionary to a file

def whatsHere(playerLocation, playerLocationNum):
    print("at the", playerLocation, "there is:")
    inv_of_location=dictionary[playerLocationNum]
    if inv_of_location==[]:
        print("nothing")
    else:
        print(inv_of_location)
    return inv_of_location#returns what is in this location

def healthCheck():
    global health
    if health<1:
        print("you have run out of health!")
    elif health>0:
        print("you now have %s health" % health)
    #checks how much health you have left

def read_market():
    global market
    items=open("items to buy.txt", "r")
    itemsSplit=items.read().splitlines()
    items.close()
    for i in range(0, len(itemsSplit)):
        for j in range(0, len(itemsSplit[i].split(" , "))):
            market[i+1].append(itemsSplit[i].split(" , ")[j])
    #reads what items are in the market at the moment

def balance():
    amount=0
    if "money" in read_inventory():
        for i in range(0, len(read_inventory())):
            if read_inventory()[i]=="money":
                amount+=1
    return amount
    #checks how much money you have

def removeFromInv(item, amount):
    inventory=read_inventory()
    inventoryw=open("inventory.txt", "w")
    count=0
    count1=0
    while count<amount:
        print(count1)
        if inventory[count1]==item:
            del(inventory[count1])
            count+=1
        count1+=1
    for i in range(0, len(inventory)):
        inventoryw.write(inventory[i]+"\n")
    inventoryw.close()
    #removes a particular item from your inventory
        


###functions relating to people you can talk to on your journey
def town_member(playerLocation, inv_of_location, playerLocationNum, dictionary):
    if playerLocation=="town":
        print("I am a town memeber, and I am poor")
        time.sleep(2)
        print("I need a house, there is a vacant one I could live in,")
        time.sleep(1)
        print("but I dont have the key! It's been lost for years!")
        time.sleep(2)
        print("if you could get me the key I would tell you a secret")
        time.sleep(1)
        print("and owe you a favour in return")
        time.sleep(2)
        choice=input("use the leave keyword to give key, or bye to go about your business")
        if choice=="bye":
            print("whenever you are in the town, use say 'town_member' to talk to me again")
            time.sleep(2)
        elif choice=="leave key":
            choiceSplit=choice.split(" ")
            leave(choiceSplit, inv_of_location, playerLocationNum, dictionary)
            for i in range(0, len(dictionary[4])):
                if dictionary[4][i]=="key":
                    del(dictionary[4][i])

def goblin(inv_of_location, playerLocationNum, dictionary):
    global health
    time.sleep(2)
    truth=input("Goblin: I see you have some supplies... maybe some food?")
    while truth!="yes" and truth!="no":
        truth=input("Goblin: will you not answer my question? Do you have supplies?")
    if truth=="yes":
        time.sleep(2)
        share=input("Goblin: would you be willing to share some?")
        if share=="yes":
            time.sleep(1)
            print("Goblin: well thank you")
            item=["supplies"]
            leave(item, inv_of_location, playerLocationNum, dictionary)
            time.sleep(2)
            print("Goblin: don't expect me to give this back...\nNot without a fight anyway...")
            time.sleep(3)
            print("Goblin: here though... have this, I found it on the beach")
            inventory=open("inventory.txt", "a")
            inventory.write("shell"+"\n")
            inventory.close()
            print(read_inventory())
        else:
            time.sleep(1)
            print("I think you'll find you will!")
            win=goblinFight()
            if win==True:
                print("you beat the goblin, and take the supplies!")
                time.sleep(2)
                print("you lose 40 health though")
                health+=-40
                healthCheck()
            elif win==False:
                print("the goblin beat you!")
                time.sleep(2)
                print("you lose the supplies, and 75 health!")
                health+=-75
                healthCheck()
    elif truth=="no":
        print("Goblin: oh ok, I'll see you later...")
        time.sleep(2)
        print("you aren't sure if you trust the goblin, but you head onto the beach")
        time.sleep(2)
        tchoice=input("what would you like to do (type quit to save and quit (and heal))?")
        print("as you are about to", tchoice, "you were jumped by the goblin behind a rock!")
        win=goblinFight()
        if win==False:
            print("the goblin hit you!")
            time.sleep(1)
            print("you lost 60 health!")
            time.sleep(1)
            print("and the supplies")
            health+=-60
            healthCheck()
            time.sleep(2)
            removeFromInv("supplies", 1)
            print("you now have:\n", read_inventory())
            dictionary[8].append("supplies")
        elif win==True:
            print("you still lose 30 health though")
            time.sleep(2)
            health+=-30
            healthCheck()
            print("one more hit should do!")
            win1=goblinFight()
            if win1==False:
                print("the goblin got you the second time...")
                time.sleep(2)
                print("you lose 40 health")
                time.sleep(1)
                print("and the supplies")
                health+=-40
                healthCheck()
                removeFromInv("supplies", 1)
                print("you now have:\n", read_inventory())
            elif win1==True:
                print("you got him again!")
                time.sleep(2)
                print("you lose 20 health")
                health+=-20
                healthCheck()
                time.sleep(2)
                print("you keep the supplies")

def goblinFight():
    win=False
    time.sleep(2)
    print("(you fight the goblin)")
    goblinAttack=random.randint(1, 3)
    yourAttack=input("do you attack: left, right, or centre?")
    attackInt==attackInt(yourAttack)
    while attackInt==goblinAttack:
        print("You both attack here and parry! Attack again!")
    if goblinAttack==2 and attackInt!=0:
        print("the goblin attacked centre and got you first")
    elif goblinAttack==3 and attackInt==1:
        print("you attacked left,\nbut to dodge the goblins right attack hit a rock instead!")
    else:
        print("you hit the goblin!")
        win=True
    return win

def attackInt(attack):
    if attack=="left":
        attackInt=1
    elif attack=="centre":
        attackInt=2
    elif attack=="right":
        attackInt=3
    else:
        print("you didn't pick an option and you lost the battle")
        yourAttackInt==0


        
###functions of actions you can do at a location normally
def go(choiceSplit, locations, playerLocation, playerLocationNum):
    for i in range(0, len(choiceSplit)):
        if choiceSplit[i] in locations:
            if ((playerLocationNum+1==locationNumFunc(choiceSplit[i])) and\
               (playerLocationNum!=1 and playerLocationNum!=5))\
                or ((playerLocationNum-1==locationNumFunc(choiceSplit[i])) and\
               (playerLocationNum!=2 and playerLocationNum!=3 and\
                    playerLocationNum!=6))\
               or (playerLocationNum+3==locationNumFunc(choiceSplit[i]))\
                   or playerLocationNum-3==locationNumFunc(choiceSplit[i]):
                #if the place you are at is to the right of where you're going
                #and you aren't in location 1 or 5 (not in 1 and not in 5)
                #or the place you are is to the left of where you're going
                #and you're not in location 2, 3, or 6 (not in 2 and not in 3...)
                #or the place you're going is above the place you are at
                #and your location isn't 6 or 8 (not 6 and not 8)
                #you are above where you're trying to go
                #and you location isn't 6 and isn't 8
                if (((playerLocationNum-3==locationNumFunc(choiceSplit[i])) and\
                   (playerLocationNum==6 or playerLocationNum==8))\
                    or ((playerLocationNum+3==locationNumFunc(choiceSplit[i])) and\
                   (playerLocationNum==3 or playerLocationNum==5)))and\
                   "rope" not in read_inventory():
                    return playerLocation
                else:
                    print("ok")
                    playerLocation=choiceSplit[i]
                    print("you are at the", playerLocation)
    return playerLocation#changes the player's location

def take(choiceSplit, inv_of_location, dictionary, playerLocation):
    taken=False
    for i in range(0, len(choiceSplit)):#for every item in choiceSplit
        for j in range(0, len(dictionary[locationNumFunc(playerLocation)])):
            #for every item in the key for this location
            if taken==True:
                j-=1
            if choiceSplit[i]==dictionary[locationNumFunc(playerLocation)][j]:
                if choiceSplit[i] in inv_of_location:
                    inventory=open("inventory.txt", "a")
                    inventory.write(choiceSplit[i]+"\n")#will add choice to inventory
                    inventory.close()
                    del(dictionary[locationNumFunc(playerLocation)][j])#deletes choice from dictionary
                    taken=True
                else:
                    print("you cannot take that, its not in", playerLocation)
    if taken==True:
        if read_inventory==[]:
            print("you have nothing")#prints if you have nothing
            return dictionary
        else:
            print("you now have", read_inventory())#prints inventory so far
            return dictionary
    else:
        print("that isn't an item in the game")
    if "rope" in read_inventory():
        print("with the rope, you can now travel between cliffs and village",\
              "\n", "and beach and windmill\nand vice versa")
    return dictionary

def leave(choiceSplit, inv_of_location, playerLocationNum, dictionary):
    left=False
    inventory=read_inventory()
    for i in range(0, len(choiceSplit)):
        if choiceSplit[i] in inventory:
            dictionary[playerLocationNum].append(choiceSplit[i])
            removeFromInv(choiceSplit[i], 1)
            left=True
    if left==True:
        if read_inventory==[]:
            print("you have nothing")#prints if you have nothing
            return dictionary
        else:
            print("you now have", read_inventory())#prints inventory so far
            return dictionary
    else:
        print("you cannot leave that item, as you don't have it")

def buy():
    global market
    amount=balance()
    if amount>0:
        print("you have %s money, and therefore can buy something!" % amount)
        time.sleep(2)
        print("you can buy:")
        read_market()#reads in what is in the markets inventory
        print(market)
        time.sleep(2)
        choice=input("what would you like to buy?")
        for i in range(1, 4):
            #for each possible cost of item
            if choice in market[i]:
                if amount<i:
                    print("you cannot afford that")
                    time.sleep(2)
                else:
                    print("let me see...")
                    for j in range(0, len(market[i])):
                        #for each item in the price range
                        if market[i][j]==choice:
                            print("Alright! We've got it!")
                            del(market[i][j])
                            marketc=open("items to buy.txt", "w")
                            marketc.write("")
                            marketc.close()
                            #clears the market inventory
                            for k in range(1, len(market)+1):
                                marketa=open("items to buy.txt", "a")
                                if len(market[k])==0:
                                    marketa.write("\n")
                                for l in range(0, len(market[k])):
                                    if l+1!=len(market[k]):
                                        marketa.write(market[k][l]+" , ")
                                    elif l+1==len(market[k]):
                                        marketa.write(market[k][l]+"\n")
                                marketa.close()
                            for k in range(1, len(market)+1):
                                market[k]=[]
                            #deletes the item you bought from market
                            inventory=open("inventory.txt", "a")
                            inventory.write(choice)
                            inventory.close()
                            #adds the item you bought to your inventory
                            removeFromInv("money", i)
                            break
                    time.sleep(2)
                    print("you now have", read_inventory())
                    time.sleep(1)
                    print("and %s money left" % balance())
                    time.sleep(2)
    else:
        print("you have no money, and so can't buy at the market")

def sell():
    global market
    choice=input("what would you like to sell?")
    if choice in read_inventory():
        price=random.randint(1, 2)
        time.sleep(2)
        print("ok, ill give you %s money for that" % price)
        time.sleep(1)
        agree=input("do you accept?")
        if agree=="yes":
            print("deal")
            inventorya=open("inventory.txt", "a")
            for i in range(0, price):
                inventorya.write("money")
            inventorya.close()
            removeFromInv(choice, 1)
            market(price).append(choice)
        else:
            print("i see, not good enough, well im giving you any mroe than that!")
            time.sleep(2)
    else:
        print("you're not fooling anyone! You don't even have that item!")
        time.sleep(2)

def use(choiceSplit, playerLocation):
    global health
    if "bandage" in choiceSplit and "bandage" in read_inventory():
        print("you used the bandage, and recovered 50 health!")
        health+=50
        healthCheck()
        removeFromInv("bandage", 1)
    if "pickaxe" in choiceSplit and playerLocation=="mine":
        print("you used the pickaxe to mine into the wall")
        time.sleep(2)
        inventorya=open("inventory.txt", "a")
        inventorya.write("rocks\n")
        inventorya.close()
        print("you gained rocks!")
        print("you now have:", read_inventory())
        


###the function to decide what happens and when
def action(choiceSplit):
    global playerLocation, playerLocationNum
    global inv_of_location, dictionary
    global town_before
    if "go" in choiceSplit:
        temp=playerLocation
        playerLocation=go(choiceSplit, locations, playerLocation, playerLocationNum)
        playerLocationNum=locationNumFunc(playerLocation)
        if temp==playerLocation:
            print("you cannot go there, try going somewhere closer")
        if town_before==False:
            if playerLocation=="town":
                if "key" in dictionary[locationNumFunc(playerLocation)]:
                    town_before=True
                town_member(playerLocation, inv_of_location, playerLocationNum, dictionary)
        if playerLocation=="beach" and "supplies" in read_inventory()\
           and temp!=playerLocation:
            goblin(inv_of_location, playerLocationNum, dictionary)
    elif "town_member" in choiceSplit:
        town_member(playerLocation, inv_of_location, playerLocationNum, dictionary)
    elif "take" in choiceSplit:
        dictionary=take(choiceSplit, inv_of_location, dictionary, playerLocation)
    elif "leave" in choiceSplit:
        dictionary=leave(choiceSplit, inv_of_location, playerLocationNum, dictionary)
    elif "use" in choiceSplit:
        use(choiceSplit, playerLocation)
    elif "market" in choiceSplit:
        buy_sell=input("would you like to buy or sell at the market?")
        if buy_sell=="buy":
            buy()
        elif buy_sell=="sell":
            sell()
        else:
            print("that wasn't an option")
    elif "quit" in choiceSplit:
        writeAllFromInv(dictionary)
        sys.exit("bye! (the error was intentional)")
    else:
        print("that wasn't recognised, try again")



###the main code for the game,
###including a loop which will re-run the action function
###until you win

#variables needed thoughout the game
dictionary={0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
market={1:[], 2:[], 3:[]}
town_before=False
won=False
health=100

newGame=new_game()#to see if you want a new game

create_dictionary()#will create the dictionary if location inventories for later

locations=read_locations()
playerLocation="village"
playerLocationNum=locationNumFunc(playerLocation)
if newGame=="yes":
    firstChoice=menu(locations, playerLocation, playerLocationNum)
    firstChoiceSplit=firstChoice.split(" ")
    action(firstChoiceSplit)
else:
    print("in you inventory you still have:")
    print(read_inventory())
while won==False:
    inv_of_location=whatsHere(playerLocation, playerLocationNum)
    print("from the", playerLocation)
    choice=input("what would you like to do (type quit to save and quit (and heal))?")
    choice=choice.split(" ")
    action(choice)
