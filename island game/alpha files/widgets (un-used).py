###Island game - widgets
###Alpha V.1.0

from tkinter import *
import time, sys
import functions
from Alpha_V1 import locations, playerLocation, playerLocationNum


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
    self.go_button["command"]=lambda: functions.go(locations, playerLocation, playerLocationNum)

def new_gameYes(self):
    self.new_gameYes=Button(self.tk, text="Yes", height=2, width=20)
    self.new_gameYes.place(relx=0.5, rely=0.5, anchor="se")
    self.new_gameYes.pi=self.new_gameYes.place_info()
    self.disappear(self.new_gameYes)

def new_gameNo(self):
    self.new_gameNo=Button(self.tk, text="No", height=2, width=20)
    self.new_gameNo.place(relx=0.85, rely=0.5, anchor="se")
    self.new_gameNo.pi=self.new_gameNo.place_info()
    self.disappear(self.new_gameNo)

def you_are_here(self):
    self.you_are_here=Text(self.tk, height=1, width=12)
    x=where_are_youX(self.playerLocationNum)
    y=where_are_youY(self.playerLocationNum)
    self.you_are_here.place(relx=x, rely=y, anchor="sw")
    self.you_are_here.insert(END, "You are here")

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
