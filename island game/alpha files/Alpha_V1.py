###Island game
###Alpha V.1.0

from tkinter import *
import time, random

import functions



###game class to create canvas
class game:
    def __init__(self, locations, playerLocation,\
                 playerLocationNum, town_before, won,\
                 dictionary, market, health):
        
        self.location=locations
        self.playerLocation=playerLocation
        self.playerLocationNum=playerLocationNum
        self.town_before=town_before
        self.won=won
        self.dictionary=dictionary
        self.market=market
        self.health=health
        
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
        
        input_box(self)
        #input box
        enter_button(self)
        #enter button
        quit_button(self)
        #quit button
        you_are_here(self)
        #you are here text
        go_button(self)
        #go button
        take_button(self)
        #take button
        new_gameYes(self)
        #yes button to new game question
        new_gameNo(self)
        #no button to new game question


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

    def disappear(self, text_box):
        text_box.place_forget()
        self.tk.update()
    def appear(self, text_box):
        text_box.place(text_box.pi)
        self.tk.update()



###class for the buttons
class text_buttons:
    def __init__(self):
        global g, t
        global playerLocation, dictionary

        ###text boxes
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

        self.text_box6=Button(g.tk, text="would you like to play a new game?", height=3, width=50)
        self.new_text(self.text_box6)

        self.text_box7=Button(g.tk, text="Off you go!", height=3, width=50)
        self.new_text(self.text_box7)

        self.text_box8=Button(g.tk, text="new save game created", height=3, width=50)
        self.new_text(self.text_box8)

        self.text_box9=Button(g.tk, text="Welcome to the island of lovely bunch of coconuts", height=3, width=50)
        self.new_text(self.text_box9)

        self.text_box10=Button(g.tk, text="you are a citizen of the village\nin the south west section of the island", height=3, width=50)
        self.new_text(self.text_box10)
        

        self.text_box1["command"]=self.text1
        self.text_box2["command"]=self.text2
        self.text_box3["command"]=self.text3
        self.text_box4["command"]=self.text4
        self.text_box5["command"]=self.text5
        self.text_box8["command"]=self.text8
        self.text_box9["command"]=self.text9
        self.text_box10["command"]=self.text10

    def text1(self):
        g.disappear(self.text_box1)
        g.appear(self.text_box2)
    def text2(self):
        g.disappear(self.text_box2)
        g.appear(self.text_box3)
    def text3(self):
        g.disappear(self.text_box3)
        g.appear(self.text_box4)
    def text4(self):
        g.disappear(self.text_box4)
        g.appear(self.text_box5)
    def text5(self):
        g.disappear(self.text_box5)
        g.appear(self.text_box6)
        g.appear(g.new_gameYes)
        g.appear(g.new_gameNo)
    def text8(self):
        g.disappear(self.text_box8)
        g.appear(self.text_box9)
    def text9(self):
        g.disappear(self.text_box9)
        g.appear(self.text_box10)
    def text10(self):
        g.disappear(self.text_box10)
        g.appear(g.go_button)
        g.appear(g.take_button)
        g.appear(g.go_button)
        g.appear(g.you_are_here)
        g.appear(t.text_box7)

    def new_text(self, name):
        name.place(relx=1.0, rely=1.0, x=-5, y=-29, anchor="se")
        name.pi=name.place_info()
        g.disappear(name)


###widgets
def input_box(self):
    self.tinput=Entry(self.tk, width=48)
    self.tinput.place(relx=1.0, rely=1.0, x=-72, y=-10, anchor="se")
    self.tinput.pi=self.tinput.place_info()

def enter_button(self):
    self.enter_button=Button(self.tk, text="enter", height=1, width=10)
    self.enter_button.place(relx=1.0, rely=1.0, x=-5, y=-5, anchor="se")
    self.enter_button.pi=self.enter_button.place_info()

def quit_button(self):
    self.quit_button=Button(self.tk, text="quit", height=1, width=10)
    self.quit_button.place(relx=1.0, rely=0.0, x=-5, y=5, anchor="ne")
    self.quit_button["command"]=self.close

def go_button(self):
    self.go_button=Button(self.tk, text="go", height=2, width=10)
    self.go_button.place(relx=0.05, rely=0.05, anchor="nw")
    self.go_button.pi=self.go_button.place_info()
    self.go_button["command"]=lambda: functions.go(locations, playerLocation, playerLocationNum)
    self.disappear(self.go_button)

def take_button(self):
    global inv_of_location
    self.take_button=Button(self.tk, text="take", height=2, width=10)
    self.take_button.place(relx=0.05, rely=0.05, anchor="nw")
    self.take_button.pi=self.take_button.place_info()
    self.take_button["command"]=lambda: functions.take(inv_of_location, dictionary, playerLocation)
    self.disappear(self.take_button)

def new_gameYes(self):
    self.new_gameYes=Button(self.tk, text="Yes", height=2, width=20)
    self.new_gameYes.place(relx=0.5, rely=0.5, anchor="se")
    self.new_gameYes.pi=self.new_gameYes.place_info()
    self.new_gameYes["command"]=new_game
    self.disappear(self.new_gameYes)

def new_gameNo(self):
    self.new_gameNo=Button(self.tk, text="No", height=2, width=20)
    self.new_gameNo.place(relx=0.85, rely=0.5, anchor="se")
    self.new_gameNo.pi=self.new_gameNo.place_info()
    self.new_gameNo["command"]=no_new_game
    self.disappear(self.new_gameNo)

def you_are_here(self):
    self.you_are_here=Text(self.tk, height=1, width=12)
    x=functions.where_are_youX(self.playerLocationNum)
    y=functions.where_are_youY(self.playerLocationNum)
    self.you_are_here.place(relx=x, rely=y, anchor="sw")
    self.you_are_here.pi=self.you_are_here.place_info()
    self.you_are_here.insert(END, "You are here")
    self.disappear(self.you_are_here)

def no_new_game():
    g.disappear(g.new_gameNo)
    g.disappear(g.new_gameYes)
    g.disappear(t.text_box6)
    g.appear(g.go_button)
    g.appear(g.take_button)
    g.appear(g.you_are_here)
    g.appear(t.text_box7)



###extra functions
def update_values():
    global playerLocation, playerLocationNum, inv_of_location
    global dictionary
    playerLocationNum=functions.locationNumFunc(playerLocation)
    inv_of_location=functions.whatsHere(playerLocationNum, dictionary)



###functions to run at the start of the game
def new_game():
    g.disappear(g.new_gameNo)
    g.disappear(g.new_gameYes)
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
    g.appear(t.text_box8)

def reset(file, backup):
    backupLines=backup.read().splitlines()
    for i in range(0, len(backupLines)):
        file.write(backupLines[i]+"\n")
        



###the main code for the game,
###including a loop which will re-run the action function
###until you win


#variables needed thoughout the game
dictionary={0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
market={1:[], 2:[], 3:[]}
town_before=False
won=False
health=100

dictionary=functions.create_dictionary(dictionary)#will create the dictionary if location inventories for later

locations=functions.read_locations()
playerLocation="village"
playerLocationNum=functions.locationNumFunc(playerLocation)


if __name__=="__main__":
    inv_of_location=functions.whatsHere(playerLocationNum, dictionary)
    g=game(locations, playerLocation, playerLocationNum, town_before, won,\
           dictionary, market, health)
    t=text_buttons()
    g.mainloop()
