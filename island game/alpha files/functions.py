###Island game - functions
###Alpha V.1.0

###functions to run thoughtout the game to find infomation e.g. read from files
def create_dictionary(dictionary):
    inv_of_everywhere=open("inventory of locations.txt", "r")
    inv_of_everywhereSplit=inv_of_everywhere.read().splitlines()
    inv_of_everywhere.close()
    for i in range(0, len(inv_of_everywhereSplit)):
        for j in range(0, len(inv_of_everywhereSplit[i].split(" , "))):
            dictionary[i].append(inv_of_everywhereSplit[i].split(" , ")[j])
            #will read all locations inventories
            #and put them into a dictionary
    return dictionary

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

def where_are_youX(playerLocationNum):
    if playerLocationNum==1 or playerLocationNum==4 or playerLocationNum==7:
        return 0.5
    if playerLocationNum==3 or playerLocationNum==6:
        return 0.27
    if playerLocationNum==5 or playerLocationNum==8:
        return 0.7

def where_are_youY(playerLocationNum):
    if playerLocationNum==6 or playerLocationNum==7 or playerLocationNum==8:
        return 0.7
    if playerLocationNum==3 or playerLocationNum==4 or playerLocationNum==5:
        return 0.5
    if playerLocationNum==1:
        return 0.3

def whatsHere(playerLocationNum, dictionary):
    inv_of_location=dictionary[playerLocationNum]
    if inv_of_location==[]:
        return "nothing"
    else:
        return inv_of_location#returns what is in this location

    

###functions of actions you can do at a location normally
def go(locations, playerLocation, playerLocationNum):
    print(playerLocation)

def take(inv_of_location, dictionary, playerLocation):
