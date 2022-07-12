###Island game
###Alpha V.1.0

from tkinter import *
import time
import sys
import random



###game class to create canvas
class game:
    def __init__(self):
        self.secs=time.gmtime()[5]
        self.mins=time.gmtime()[4]
        self.tk=Tk()
        self.tk.title("Island game Alpha V.1.0")
        #names the window
        self.canvas=Canvas(self.tk, width=500, height=500)
        self.canvas.pack()
        self.tk.update()
        self.bg=PhotoImage(file="background.gif")
        #uses the right file for the background
        w=self.bg.width()
        h=self.bg.height()
        for x in range(0, 5):
            for y in range(0, 5):
                self.canvas.create_image(x*w, y*h, image=self.bg, anchor="nw")
                #creates the canvas to the right size
        self.tinput=Entry(self.tk, width=48)
        self.tinput.place(relx=1.0, rely=1.0, x=-72, y=-10, anchor="se")
        self.tinput.pi=self.tinput.place_info()
        #input box
        self.enter_button=Button(self.tk, text="enter", height=1, width=10)
        self.enter_button.place(relx=1.0, rely=1.0, x=-5, y=-5, anchor="se")
        self.enter_button.pi=self.enter_button.place_info()
        #enter button
        self.quit_button=Button(self.tk, text="quit", height=1, width=10)
        self.quit_button.place(relx=1.0, rely=0.0, x=-5, y=5, anchor="ne")
        self.quit_button["command"]=self.close


    def buttonInput(self):
        global userInput
        userInput=self.tinput.get()

    def clearEntry(self):
        self.tinput.delete(0, 'end')
            
    def updateSleep(self, dur):
        dur=int(dur*100)
        for i in range(0, dur):
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)
            #to sleep for a certain time while still updating the canvas

    def close(self):
        self.tk.destroy()

    def mainloop(self):
        while True:
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)



###class for the buttons
class text_buttons:
    def __init__(self):
        global g
        self.text_box1=Button(g.tk, text="this is the text button", height=3, width=50)
        self.text_box1.place(relx=1.0, rely=1.0, x=-5, y=-29, anchor="se")
        self.text_box1.pi=self.text_box1.place_info()

        self.text_box2=Button(g.tk, text="It is used to relay and send information to you!", height=3, width=50)
        self.new_text(self.text_box2)

        self.text_box3=Button(g.tk, text="keep an eye on it,\nas it may contain crucial information for you", height=3, width=50)
        self.new_text(self.text_box3)

        self.text_box4=Button(g.tk, text="below is the text entry box,\nwhen a question is asked,\nenter text into it", height=3, width=50)
        self.new_text(self.text_box4)

        self.text_box5=Button(g.tk, text="when you have entered the text,\npress the enter button", height=3, width=50)
        self.new_text(self.text_box5)

        self.text_box1["command"]=self.text1
        self.text_box2["command"]=self.text2
        self.text_box3["command"]=self.text3
        self.text_box4["command"]=self.text4
        self.text_box5["command"]=self.text5

    def text1(self):
        self.disappear(self.text_box1)
        self.appear(self.text_box2)
    def text2(self):
        self.disappear(self.text_box2)
        self.appear(self.text_box3)
    def text3(self):
        self.disappear(self.text_box3)
        self.appear(self.text_box4)
    def text4(self):
        self.disappear(self.text_box4)
        self.appear(self.text_box5)
    def text5(self):
        self.disappear(self.text_box5)
        #self.appear(self.text_box6)


    def disappear(self, text_box):
        text_box.place_forget()
        g.tk.update()
    def appear(self, text_box):
        text_box.place(text_box.pi)
        g.tk.update()

    def new_text(self, name):
        name.place(relx=1.0, rely=1.0, x=-5, y=-29, anchor="se")
        name.pi=name.place_info()
        self.disappear(name)



###functions to run at the start of the game
def new_game():
    global userInput
    g.updateSleep(5)
    displayText("would you like to play a new game?")
    newGame=""
    while newGame!="yes" and newGame!="no":
        newGame=wait_for_input("would you like to play a new game\nenter yes or no")
        pass
    g.clearEntry()
    if newGame=="no":
        displayText("ok")
        g.updateSleep(2)
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
        displayText("new save game created")
    return newGame

def reset(file, backup):
    backupLines=backup.read().splitlines()
    for i in range(0, len(backupLines)):
        file.write(backupLines[i]+"\n")



###functions to run thoughtout the game to find infomation e.g. read from files
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


def wait_for_input(text_while_input):
    global userInput
    displayText(text_while_input)
    userInput=g.tinput.get()
    newGame=userInput
    g.updateSleep(2)
    return newGame



###the main code for the game,
###including a loop which will re-run the action function
###until you win


#variables needed thoughout the game
dictionary={0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
market={1:[], 2:[], 3:[]}
town_before=False
won=False
health=100
userInput=""

create_dictionary()#will create the dictionary if location inventories for later

locations=read_locations()
playerLocation="village"
playerLocationNum=locationNumFunc(playerLocation)

g=game()
b=text_buttons()
g.mainloop()
#newGame=new_game()#to see if you want a new game
