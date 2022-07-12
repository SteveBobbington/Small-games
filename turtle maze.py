from turtle import Turtle, Screen
import math
import sys

turtle_1 = Turtle(shape='turtle', visible=False)
turtle_1.color('black')
turtle_1.penup()
turtle_1.write("Ignore this screen until you pick a level", font=("Arial", 10, "normal"))
#a function to move the turtle forward and check its position is "possible"
def forward():
    global walls
    global f_or_d
    f_or_d="forward"
    turtle_1.forward(10)
    win_check()
    correctpos(turtle_1)
    for i in walls:
        inwall=isinwall(turtle_1, i)
        wheninwall(turtle_1, inwall)

#will turn the turtle right
def right():
    turtle_1.right(90)

#will turn the turtle left
def left():
    turtle_1.left(90)

#a function to move the turtle backward and check its position is "possible"
def backward():
    global f_or_d
    f_or_d="backward"
    turtle_1.backward(10)
    win_check()
    correctpos(turtle_1)
    for i in walls:
        inwall=isinwall(turtle_1, i)
        wheninwall(turtle_1, inwall)

#will lift up the pen or drop it down (for when you finish the level)
def space():
    if turtle_1.isdown()==True:
        turtle_1.up()
    else:
        turtle_1.down()

#will fix the turtles position if its "broken"
def correctpos(turtle):
    turtle.setposition(int(round(turtle.xcor(), -1)), int(round(turtle.ycor(), -1)))
    print(turtle_1.xcor(), turtle_1.ycor())

#will check if the turtle is inside a wall
def isinwall(turtle, wall):
    global border_coord
    if (turtle.xcor(), turtle.ycor()) in wall:
        return True
    elif turtle.xcor()<-border_coord or turtle.xcor()>border_coord:
        return True
    elif turtle.ycor()<-border_coord or turtle.ycor()>border_coord:
        return True
    else:
        return False

#if the last function returns true, then the turtle is in a wall
    #so it will get the turtle out the wall
def wheninwall(turtle, inwall):
    global ended
    if ended==False:
        if inwall==True:
            global f_or_d
            turtle.right(180)
            if f_or_d=="forward":
                turtle.forward(10)
            else:
                turtle.backward(10)

#will draw the wall from the list of co-ordinates
def draw_wall(turtle, positions):
    turtle.penup()
    turtle.setposition(positions[0])
    turtle.pendown()
    for position in positions[1:]:
        turtle.setposition(position)

#checks if one turtle is touching another
def iscollision(t1, t2):
    d = math.sqrt((t2.xcor() - t1.xcor()) ** 2 + (t2.ycor() - t1.ycor()) ** 2)
    return d < 20.0

#will clear the screen of all ink
def clearall():
    turtle_1.clear()
    maze_1.clear()
    maze_2.clear()
    maze_3.clear()
    goal.clear()
    border.clear()

#will produce the ending screen
def end():
    global ended
    ended=True
    clearall()
    turtle_1.setposition(0, -50)
    end=Turtle(visible=False)
    end.up()
    end.setposition(-150, 0)
    end.down()
    end.write("Good job!", font=("Arial", 50, "normal"))
    turtle_1.down()
    end.up()
    end.setposition(-150, 150)
    end.down()
    end.write("(draw something)", font=("Arial", 10, "normal"))
    end.up()
    end.setposition(-150, 100)
    end.write("(space to lift the pen)", font=("Arial", 10, "normal"))
    screen.onkey(space, "space")
    goal.setposition(1000, 1000)
    print("you may now close turtle")
    screen.exitonclick()

#will print out the menu and take a choice
def menu():
    print("which level do you play?")
    print("so far there are 3 levels!")
    print("or press 0 to quit")
    while True:
        try:
            level=int(input("which level?"))
            break
        except ValueError:
            print("that's not even a number! (I can tell)")
    return level

def draw_walls():
    wall_1=draw_wall_1()
    draw_wall(maze_1, wall_1)
    wall_2=draw_wall_2()
    draw_wall(maze_1, wall_2)
    wall_3=draw_wall_3()
    draw_wall(maze_1, wall_3)
    wall_4=draw_wall_4()
    draw_wall(maze_2, wall_4)
    wall_5=draw_wall_5()
    draw_wall(maze_3, wall_5)
    wall_6=draw_wall_6()
    draw_wall(maze_3, wall_6)
    wall_7=draw_wall_7()
    draw_wall(maze_3, wall_7)
    wall_8=draw_wall_8()
    draw_wall(maze_3, wall_8)
    wall_9=draw_wall_9()
    draw_wall(maze_3, wall_9)
    wall_10=draw_wall_10()
    draw_wall(maze_3, wall_10)

#this is a function for
def play_level(border_pos, border_size, goal_pos, start_pos,\
               wall_1, wall_2, wall_3, wall_4, wall_5, wall_6,\
               wall_7, wall_8, wall_9, wall_10):
    global choice
    global turtle_1
    global maze_1
    global maze_2
    global maze_3
    global goal
    global border
    global walls
    global border_coord
    screen=Screen()
    border_coord=border_size/2-10
    level=choice
    print("level", choice, "has opened in the other window")
    # border
    border = Turtle(visible=False)
    border.penup()
    border.pensize(10)
    border.pencolor('black')
    border.setposition(border_pos)
    border.pendown()
    border.speed("fastest")

    #will make the screen to be played on
    screen.setup(1000, 1000)
    screen.bgcolor('white')

    #draws the border
    for _ in range(4):
        border.forward(border_size)
        border.left(90)

    maze_1 = Turtle(visible=False)
    maze_1.pensize(10)
    maze_1.pencolor('black')
    maze_1.speed("fastest")

    maze_2 = Turtle(visible=False)
    maze_2.pensize(10)
    maze_2.pencolor('black')
    maze_2.speed("fastest")

    maze_3 = Turtle(visible=False)
    maze_3.pensize(10)
    maze_3.pencolor('black')
    maze_3.speed("fastest")

    # end goal
    goal = Turtle(shape='circle')
    goal.color('gold')
    goal.penup()
    goal.setposition(goal_pos)

    turtle_1 = Turtle(shape='turtle', visible=False)
    turtle_1.color('black')
    turtle_1.penup()

    turtle_1.setposition(start_pos)

    #will draw each section of wall with different maze drawing turtles
    draw_walls()

    walls=[wall_1, wall_2, wall_3, wall_4,\
           wall_5, wall_6, wall_7, wall_7,\
           wall_8, wall_9, wall_10]

    turtle_1.st()

walls=[]
#will play the game depending on the level chosen
choice=-1
def play_game():
    global choice
    global turtle_1
    global maze_1
    global maze_2
    global maze_3
    global goal
    global border
    global turtle_1
    global ended
    global walls
    global draw_wall_1
    global draw_wall_2
    global draw_wall_3
    global draw_wall_4
    global draw_wall_5
    global draw_wall_6
    global draw_wall_7
    global draw_wall_8
    global draw_wall_9
    global draw_wall_10
    if choice==-1:
        choice=menu()
        turtle_1.clear()
    if choice!=0 or ended==True:
        ended=False
        screen=Screen()
        screen.onkey(forward, "Up")
        screen.onkey(right, "Right")
        screen.onkey(left, "Left")
        screen.onkey(backward, "Down")
        screen.listen()
    if choice==1:
        def draw_wall_1():
            wall_1=[]
            wall_1.append((0, -100))
            for i in range(-100, 60, 10):
                wall_1.append((0, i))
            return wall_1

        def draw_wall_2():
            wall_2=[]
            wall_2.append((0, 0))
            for i in range(0, 70, 10):
                wall_2.append((i, 0))
            return wall_2

        def draw_wall_3():
            wall_3=[]
            wall_3.append((0, 0))
            return wall_3

        def draw_wall_4():
            wall_4=[]
            wall_4.append((0, 0))
            return wall_4

        def draw_wall_5():
            wall_5=[]
            wall_5.append((0, 0))
            return wall_5

        def draw_wall_6():
            wall_6=[]
            wall_6.append((0, 0))
            return wall_6

        def draw_wall_7():
            wall_7=[]
            wall_7.append((0, 0))
            return wall_7

        def draw_wall_8():
            wall_8=[]
            wall_8.append((0, 0))
            return wall_8

        def draw_wall_9():
            wall_9=[]
            wall_9.append((0, 0))
            return wall_9

        def draw_wall_10():
            wall_10=[]
            wall_10.append((0, 0))
            return wall_10
        level_played=play_level((-100, -100), 200, (40, -50), (-50, -50),\
                   draw_wall_1(), draw_wall_2(),draw_wall_3(), draw_wall_4(),\
                   draw_wall_5(), draw_wall_6(), draw_wall_7(), draw_wall_8(),\
                   draw_wall_9(), draw_wall_10())
        #############################where the code for level 2 starts
    elif choice==2:
        def draw_wall_1():
            wall_1=[]
            wall_1.append((-100, -200))
            for i in range(-200, -40, 10):
                wall_1.append((-100, i))
            for i in range(-100, 10, 10):
                wall_1.append((i, -50))
            for i in range(-130, -50, 10):
                wall_1.append((0, i))
            wall_1.append((0, -120))
            return wall_1

        def draw_wall_2():
            wall_2=[]
            wall_2.append((50, -200))
            for i in range(-200, 60, 10):
                wall_2.append((50, i))
            wall_2.append((50, -80))
            for i in range(50, 160, 10):
                wall_2.append((i, -80))
            wall_2.append((100, -80))
            for i in range(-140, -70, 10):
                wall_2.append((100, i))
            return wall_2

        def draw_wall_3():
            wall_3=[]
            wall_3.append((-200, 100))
            for i in range(-200, 10, 10):
                wall_3.append((i, 100))
            for i in range(0, 110, 10):
                wall_3.append((0, i))
            wall_3.append((0, 0))
            for i in range(-110, 10, 10):
                wall_3.append((i, 0))
            wall_3.append((-110, 0))
            for i in range(0, 60, 10):
                wall_3.append((-110, i))
            return wall_3

        def draw_wall_4():
            wall_4=[]
            wall_4.append((200, 50))
            for i in range(100, 210, 10):
                wall_4.append((i, 50))
            wall_4.append((100, 50))
            for i in range(50, 150, 10):
                wall_4.append((100, i))
            return wall_4

        def draw_wall_5():
            wall_5=[]
            wall_5.append((0, 0))
            return wall_5

        def draw_wall_6():
            wall_6=[]
            wall_6.append((0, 0))
            return wall_6

        def draw_wall_7():
            wall_7=[]
            wall_7.append((0, 0))
            return wall_7

        def draw_wall_8():
            wall_8=[]
            wall_8.append((0, 0))
            return wall_8

        def draw_wall_9():
            wall_9=[]
            wall_9.append((0, 0))
            return wall_9

        def draw_wall_10():
            wall_10=[]
            wall_10.append((0, 0))
            return wall_10
        level_played=play_level((-200, -200), 400, (-150, 150), (-150, -150),\
                   draw_wall_1(), draw_wall_2(),draw_wall_3(), draw_wall_4(),\
                   draw_wall_5(), draw_wall_6(), draw_wall_7(), draw_wall_8(),\
                   draw_wall_9(), draw_wall_10())
        #############################where the code for level 3 starts
    elif choice==3:
        #different functions for each section of the wall
        def draw_wall_1():
            wall_1=[]
            for i in range(0,310,10):
                wall_1.append((i,-450))
            wall_1.append((0, -450))
            for i in range(0, 160, 10):
                wall_1.append((i, -250))
            wall_1.append((0, -250))
            for i in range(50, 260, 10):
                negi=-i
                wall_1.append((0, negi))
            for i in range(0, 110, 10):
                wall_1.append((i, -50))
            for i in range(50, 460, 10):
                negi=-i
                wall_1.append((0, negi))
            return wall_1

        def draw_wall_2():
            wall_2=[]
            for i in range(-150, 460, 10):
                negi=-i
                wall_2.append((300, negi))
            wall_2.append((300, 150))
            for i in range(100, 310, 10):
                wall_2.append((i, 150))
            for i in range(50, 110, 10):
                wall_2.append((300, i))
            wall_2.append((300, 50))
            for i in range(100, 310, 10):
                wall_2.append((i, 50))
            for i in range(-150, 60, 10):
                wall_2.append((300, i))
            wall_2.append((300, -150))

            for i in range(100, 310, 10):
                wall_2.append((i, -150))
            for i in range(-450, -160, 10):
                wall_2.append((300, i))
            return wall_2

        def draw_wall_3():
            wall_3=[]
            for i in range(-450, 460, 10):
                wall_3.append((450, i))
            for i in range(450, 200, 10):
                wall_3.append((i, 450))
            wall_3.append((200, 450))
            for i in range(400, 460, 10):
                wall_3.append((200, i))
            wall_3.append((200, 400))
            for i in range(50, 210, 10):
                wall_3.append((i, 400))
            wall_3.append((50, 400))
            for i in range(350, 410, 10):
                wall_3.append((50, i))
            wall_3.append((50, 350))
            for i in range(0, 60, 10):
                wall_3.append((i, 350))
            wall_3.append((0, 350))
            for i in range(350, 410, 10):
                wall_3.append((0, i))
            for i in range(-200, 10, 10):
                wall_3.append((i, 400))
            wall_3.append((-200, 400))
            for i in range(350, 410, 10):
                wall_3.append((-200, i))
            wall_3.append((-200, 350))
            for i in range(-270, -210, 10):
                wall_3.append((i, 350))
            wall_3.append((-270, 350))
            for i in range(350, 410, 10):
                wall_3.append((-270, i))
            wall_3.append((-270, 400))
            for i in range(250, 410, 10):
                wall_3.append((-270, i))
            return wall_3

        def draw_wall_4():
            wall_4=[]
            wall_4.append((300, 150))
            for i in range(100, 310, 10):
                wall_4.append((i, 150))
            wall_4.append((100, 150))
            for i in range(150, 210, 10):
                wall_4.append((100, i))
            for i in range(-200, 100, 10):
                wall_4.append((i, 200))
            wall_4.append((-200, 200))
            for i in range(150, 210, 10):
                wall_4.append((-200, i))
            wall_4.append((-200, 150))
            for i in range(-350, -210, 10):
                wall_4.append((i, 150))
            wall_4.append((-350, 150))
            for i in range(150, 410, 10):
                wall_4.append((-350, i))
            return wall_4

        def draw_wall_5():
            wall_5=[]
            wall_5.append((-270, 150))
            for i in range(0, 160, 10):
                wall_5.append((-270, i))
            wall_5.append((-270, 0))
            for i in range(-270, -200, 10):
                wall_5.append((i, 0))
            for i in range(0, 60, 10):
                wall_5.append((-200, i))
            for i in range(-200, -140, 10):
                wall_5.append((i, 50))
            for i in range(50, 110, 10):
                wall_5.append((-150, i))
            for i in range(-150, -100):
                wall_5.append((i, 100))
            for i in range(100, 160, 10):
                wall_5.append((-100, i))
            for i in range(-100, -40, 10):
                wall_5.append((i, 150))
            wall_5.append((-100, 150))
            for i in range(100, 160, 10):
                wall_5.append((-100, i))
            wall_5.append((-100, 100))
            for i in range(-150, -90, 10):
                wall_5.append((i, 100))
            wall_5.append((-150, 100))
            for i in range(50, 110, 10):
                wall_5.append((-150, i))
            wall_5.append((-150, 50))
            for i in range(-200, -140, 10):
                wall_5.append((i, 50))
            wall_5.append((-200, 50))
            for i in range(0, 60, 10):
                wall_5.append((-200, i))
            wall_5.append((-200, 0))
            for i in range(-270, -200, 10):
                wall_5.append((i, 0))
            wall_5.append((-270, 0))
            for i in range(-150, 10, 10):
                wall_5.append((-270, i))
            wall_5.append((-270, -150))
            for i in range(-350, -270, 10):
                wall_5.append((i, -150))
            wall_5.append((-350, -150))
            for i in range(-350, -270, 10):
                wall_5.append((i, -150))
            wall_5.append((-270, -150))
            for i in range(-250, -140, 10):
                wall_5.append((-270, i))
            wall_5.append((-270, -250))
            for i in range(-350, -270, 10):
                wall_5.append((i, -250))
            wall_5.append((-350, -250))
            for i in range(-350, -190, 10):
                wall_5.append((i, -250))
            for i in range(-350, -240, 10):
                wall_5.append((-200, i))
            wall_5.append((-200, -350))
            return wall_5

        def draw_wall_6():
            wall_6=[]
            wall_6.append((-300, -450))
            for i in range(-450, -340, 10):
                wall_6.append((-300, i))
            wall_6.append((-300, -450))
            for i in range(-300, -90, 10):
                wall_6.append((i, -450))
            for i in range(-450, -340, 10):
                wall_6.append((-100, i))
            wall_6.append((-100, -450))
            for i in range(-100, 460, 10):
                wall_6.append((i, -450))
            for i in range(-450, -260, 10):
                wall_6.append((450, i))
            wall_6.append((450, 250))
            for i in range(200, 460, 10):
                wall_6.append((i, 250))
            for i in range(250, 460, 10):
                wall_6.append((450, i))
            for i in range(300, 460, 10):
                wall_6.append((i, 450))
            wall_6.append((300, 450))
            for i in range(300, 460, 10):
                wall_6.append((300, i))
            wall_6.append((300, 300))
            for i in range(300, 360, 10):
                wall_6.append((300, i))
            for i in range(300, 360):
                wall_6.append((i, 350))
            return wall_6

        def draw_wall_7():
            wall_7=[]
            wall_7.append((-450, 0))
            for i in range(-450, -340, 10):
                wall_7.append((i, 0))
            return wall_7

        def draw_wall_8():
            wall_8=[]
            wall_8.append((0, -200))
            for i in range(-100, 10, 10):
                wall_8.append((i, -200))
            wall_8.append((-100, -200))
            for i in range(-200, -90, 10):
                wall_8.append((-100, i))
            for i in range(-150, -90, 10):
                wall_8.append((i, -100))
            wall_8.append((-150, -100))
            return wall_8

        def draw_wall_9():
            wall_9=[]
            wall_9.append((0, 0))
            return wall_9

        def draw_wall_10():
            wall_10=[]
            wall_10.append((0, 0))
            return wall_10

        level_played=play_level((-450, -450), 900, (375, -350), (100, -300),\
                   draw_wall_1(), draw_wall_2(),draw_wall_3(), draw_wall_4(),\
                   draw_wall_5(), draw_wall_6(), draw_wall_7(), draw_wall_8(),\
                   draw_wall_9(), draw_wall_10())

    elif choice==0:
        sys.exit("bye then! (the error is intentional alright!)\n(turtle may or may not crash)")
    else:
        print("that was not a choice")

def win_check():
    if iscollision(turtle_1, goal):
        goal.hideturtle()
        end()

play_game()
screen=Screen()
screen.mainloop()

print("You have closed turtle... Good job")
print("would you like to play this level again? ('again')")
print("play the next level? ('next')")
now=input("or quit? ('quit')")
while now!="again" and now!="next" and now!="quit":
    print("that wasn't a choice")
    now=input("now try again")
if now=="again":
    play_game()
elif now=="next":
    choice+=1
    play_game()
elif now=="quit":
    sys.exit("bye then! (the error is intentional alright!)")
