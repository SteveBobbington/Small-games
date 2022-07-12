import time
bread=0
pickle=0
butter=0
cheese=0
bread_knife=0
pickle_knife=0
butter_knife=0
cheese_knife=0
un_opened=0
un_cut=1
on_table=2
in_hand=3
in_sandwich=4
all_items=["bread", "pickle", "butter", "cheese", "bread_knife", \
               "pickle_knife", "butter_knife", "cheese_knife", "un_opened", \
               "un_cut", "on_table", "in_hand", "in_sandwich"]
careful=False
choice=0

def input_packets():
    global bread
    global cheese
    global pickle
    global butter
    bread=int(input("is the bread in a packet? If it is type 0, if it isnt type 1"))
    butter=int(input("is the butter in a packet? If it is type 0, if it isnt type 1"))
    pickle=int(input("is the pickle in a packet? If it is type 0, if it isnt type 1"))
    cheese=int(input("is the cheese in a packet? If it is type 0, if it isnt type 1"))

def input_cutting():
    global bread
    global cheese
    global pickle
    global butter
    bread=int(input("does the bread need cutting? If it does type 1, if it doesn't type 2"))
    pickle=int(input("does the pickle need cutting? If it does type 1, if it doesn't type 2"))
    cheese=int(input("does the cheese need cutting? If it does type 1, if it doesn't type 2"))

def cut(knife, item):
    global careful
    global in_hand
    global on_table
    time.sleep(2)
    print("preparing to cut item")
    if careful==True:
        print("you were careful with the knife")
    knife=in_hand
    item=in_hand
    time.sleep(2)
    print("item has been cut")
    knife=on_table
    item=on_table

def open(knife, item):
    global careful
    time.sleep(2)
    print("preparing to open item")
    if careful==True:
        print("you were careful with the knife")
    global in_hand
    global on_table
    knife=in_hand
    item=in_hand
    time.sleep(2)
    print("item has been opened")
    knife=on_table
    item=on_table

def spread(knife, item):
    global in_hand
    global on_table
    global in_sandwich
    global careful
    print("preparing to spread item")
    if careful==True:
        print("you were careful with the knife")
    knife=in_hand
    item=in_hand
    time.sleep(2)
    print("picked up items needed")
    knife=on_table
    print("item has now been spread")
    
def menu():
    global careful
    global choice
    while choice==0:
        print("press 1 to look at all items needed in the sandwich making process")
        print("press 2 to be careful with knifes in the future")
        print("press 3 to make a sandwich!")
        print("press 4 to quit and leave the sandwiches alone in the dark")
        choice=int(input("what do you press?"))
        if choice==1:
            print(all_items)
            time.sleep(2)
            choice=0
        elif choice==2:
            careful=True
            time.sleep(2)
            choice=0
        elif choice==3:
            how_many_sandwiches()
        elif choice==4:
            print("the sandwiches are now sad")
            return

def make_sandwich():
    global in_hand
    global on_table
    global in_sandwich
    global un_opened
    global un_cut
    global bread
    global cheese
    global pickle
    global butter
    global bread_knife
    global cheese_knife
    global pickle_knife
    global butter_knife
    global choice
    input_packets()
    if bread==un_opened:
        print("bread needs to be opened")
        open(bread_knife, bread)
    if cheese==un_opened:
        print("cheese needs to be opened")
        open(cheese_knife, cheese)
    if butter==un_opened:
        print("butter needs to be opened")
        open(butter_knife, butter)
    if pickle==un_opened:
        print("pickle needs to be opened")
        open(pickle_knife, pickle)
    input_cutting()
    if bread==un_cut:
        print("bread needs to be cut")
        cut(bread_knife, bread)
    slices=int(input("as bread is cut now, how many slices?"))
    while slices<1:
        print("sorry, cannot make sandwich with less than 1 slices")
        slices=int(input("so how many slices really?"))
    if slices==1:
        print("will collect and use 1 slice")
    elif slices==2:
        print("will collect and use 2 slices")
    elif slices==3:
        print("will collect and use 3 slices")
    elif slices==4:
        print("will collect and use 4 slices")
    elif slices>4:
        print("wow! that many? thats a lot of sandwich... ok, using that many slices...")
    if cheese==un_cut:
        print("cheese needs to be cut")
        cut(cheese_knife, cheese)
    if pickle==un_cut:
        print("pickle needs to be sliced")
        cut(pickle_knife, pickle)
    print("all ingredients are now ready!")
    print("let the sandwich making commence!")
    bread=in_sandwich
    time.sleep(2)
    print("butter needs to be spread")
    spread(butter_knife, butter)
    butter=in_sandwich
    time.sleep(2)
    print("putting cheese in sandwich")
    time.sleep(2)
    cheese=in_sandwich
    print("placing pickles")
    time.sleep(2)
    pickle=in_sandwich
    if cheese==in_sandwich and bread==in_sandwich and butter==in_sandwich and pickle==in_sandwich:
        print("sandwich has now been made as all ingredients report as 'in_sandwich'!!!")
        print("(now you eat it)")
        if careful==False:
            print("unfortuately you were not careful with the knife, and you sandwich is all wonky")
            print("you also might need a plaster if you accidentally cut your finger off or something")
        time.sleep(2)
        choice=0

def how_many_sandwiches():
    how_many=int(input("how many sandwiches do you want to make"))
    for i in range(how_many):
        print("making sandwich number", (i+1))
        make_sandwich()
    print("all sandwiches have now been made!")

menu()
