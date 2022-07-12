import pygame
import player_class

class Card:
    def __init__(self, Xpos, Ypos, yours):
        self.font=pygame.font.SysFont("DTM-Mono", 72)
        self._rect=pygame.Rect(Xpos, Ypos, 120, 180)
        self._yours=yours
        self._cost=0
        self._original_defence=0
        self._original_attack=0
        self._defence=0
        self._attack=0
        self._effect=None
        self._effect_text=""
        self._picture=pygame.image.load("pictures/temp picture.png")
        self._type1="none"
        self._type2="none"
        self.name="Card"
        #effects
        self.taunt=False
        self.thorns=False
        self.paralysis=1
        self.transparency=False
        self.annoying=False
        self.original_dodge=0
        self.dodge=0
        self.splash=0

    def get_rect(self):
        return self._rect

    def get_cost(self):
        return self._cost

    def get_yours(self):
        return self._yours

    def get_type1(self):
        return self._type1

    def get_type2(self):
        return self._type2

    def get_attack(self):
        return self._attack

    def get_defence(self):
        return self._defence

    def change_yours(self):
        if self._yours:
            self._yours=False
        else:
            self._yours=True

    def change_attack(self, amount):
        self._attack+=amount

    def change_defence(self, amount):
        self._defence+=amount

    def silence(self):
        self.taunt=False
        self.thorns=False
        self.paralysis=0
        self.transparency=False
        self.annoying=False
        self.original_dodge=0
        self._attack=self._original_attack
        self._defence=self._original_defence

    def is_pressed(self):
        click=pygame.mouse.get_pressed()
        if click[0]==1:
            if self._rect.collidepoint(pygame.mouse.get_pos()):
                return True

    def is_hovered(self):
        if self._rect.collidepoint(pygame.mouse.get_pos()):
            return True

    def change_pos(self, newX, newY):
        self._rect=pygame.Rect(newX, newY, 120, 180)

    def magic_test(self):
        return False

    def magic(self, card, current_player, other_player, board):
        pass

    def draw(self, screen):
        if self._type2=="fighter":
            if self.is_hovered():
                self.image=pygame.image.load("pictures/hovered fighter.png")
                self.image=pygame.transform.scale(self.image, (self._rect[2], self._rect[3]))
            elif self.paralysis>1:
                self.image=pygame.image.load("pictures/paralyzed fighter.png")
                self.image=pygame.transform.scale(self.image, (self._rect[2], self._rect[3]))
            else:
                self.image=pygame.image.load("pictures/fighter.png")
                self.image=pygame.transform.scale(self.image, (self._rect[2], self._rect[3]))
        elif self._type2=="spell":
            if self.is_hovered():
                self.image=pygame.image.load("pictures/hovered spell.png")
                self.image=pygame.transform.scale(self.image, (self._rect[2], self._rect[3]))
            else:
                self.image=pygame.image.load("pictures/spell.png")
                self.image=pygame.transform.scale(self.image, (self._rect[2], self._rect[3]))
        elif self._type2=="empty":
            if self.is_hovered():
                self.image=pygame.image.load("pictures/pressed empty.png")
                self.image=pygame.transform.scale(self.image, (self._rect[2], self._rect[3]))
            else:
                self.image=pygame.image.load("pictures/empty.png")
                self.image=pygame.transform.scale(self.image, (self._rect[2], self._rect[3]))
        if self.name!="Empty":
            #name text
            self.name_text=self.font.render(self.name, True, pygame.Color("white"))
            self.name_text_rect=pygame.Rect(self._rect[0]+40, self._rect[1]+5, 40, 15)
            self.name_text=pygame.transform.scale(self.name_text, (40, 15))
            #cost text
            self.cost_text=self.font.render(str(self._cost), True, pygame.Color("deepskyblue"))
            self.cost_text_rect=pygame.Rect(self._rect[0]+96, self._rect[1]+5, 17, 15)
            self.cost_text=pygame.transform.scale(self.cost_text, (17, 15))
            #attack text
            self.attack_text=self.font.render(str(self._attack), True, pygame.Color("red"))
            self.attack_text_rect=pygame.Rect(self._rect[0]+7, self._rect[1]+161, 17, 15)
            self.attack_text=pygame.transform.scale(self.attack_text, (17, 15))
            #defence text
            self.defence_text=self.font.render(str(self._defence), True, pygame.Color("chartreuse2"))
            self.defence_text_rect=pygame.Rect(self._rect[0]+97, self._rect[1]+161, 17, 15)
            self.defence_text=pygame.transform.scale(self.defence_text, (17, 15))
            #picture
            self.picture_rect=pygame.Rect(self._rect[0]+15, self._rect[1]+30, 100, 50)
            self._picture=pygame.transform.scale(self._picture, (100, 50))
            #type1
            if self._type1=="vs":
                self.type1_image=pygame.image.load("pictures/vs type.png")
            elif self._type1=="turtle":
                self.type1_image=pygame.image.load("pictures/turtle type.png")
            self.type1_rect=pygame.Rect(self._rect[0]+3, self._rect[1]+3, 15, 20)
            self.type1_image=pygame.transform.scale(self.type1_image, (15, 20))
            #type2
            if self._type2=="fighter":
                self.type2_image=pygame.image.load("pictures/fighter type.png")
            elif self._type2=="spell":
                self.type2_image=pygame.image.load("pictures/spell type.png")
            self.type2_rect=pygame.Rect(self._rect[0]+20, self._rect[1]+3, 15, 20)
            self.type2_image=pygame.transform.scale(self.type2_image, (15, 20))
            #blit texts and image
            screen.blit(self.image, self._rect)
            screen.blit(self.name_text, self.name_text_rect)
            screen.blit(self.cost_text, self.cost_text_rect)
            if self._type2=="fighter":
                screen.blit(self.attack_text, self.attack_text_rect)
                screen.blit(self.defence_text, self.defence_text_rect)
            screen.blit(self._picture, self.picture_rect)
            screen.blit(self.type1_image, self.type1_rect)
            screen.blit(self.type2_image, self.type2_rect)
            #effect text
            split_effect_text=self._effect_text.split(" ")
            X=self._rect[0]+5
            Y=self._rect[1]+100
            for i in range(0, len(split_effect_text)):
                count=len(split_effect_text[i])
                if i>0:
                    X+=5*len(split_effect_text[i-1])+5
                if X>self._rect[0]+(120-(5*len(split_effect_text[i]))):
                    Y+=15
                    X=self._rect[0]+5
                word=self.font.render(split_effect_text[i], True, pygame.Color("white"))
                word_rect=pygame.Rect(X, Y, 5*count, 10)
                word=pygame.transform.scale(word, (5*count, 10))
                screen.blit(word, word_rect)
        else:
            screen.blit(self.image, self._rect)

class Empty(Card):
    def __init__(self, Xpos, Ypos, yours):
        super().__init__(Xpos, Ypos, yours)
        self.name="Empty"
        self._type2="empty"

class Spell_slot(Card):
    def __init__(self, Xpos, Ypos, yours):
        super().__init__(Xpos, Ypos, yours)
        self.name="Empty"
        self._type2="empty"

class Fighter_card(Card):
    def __init__(self, Xpos, Ypos, yours):
        super().__init__(Xpos, Ypos, yours)
        self.name="Fighter"
        self._type2="fighter"

class Spell_card(Card):
    def __init__(self, Xpos, Ypos, yours):
        super().__init__(Xpos, Ypos, yours)
        self.name="Spell"
        self._type2="spell"

#vs cards
class Patrick(Fighter_card):
    def __init__(self, Xpos, Ypos, yours):
        super().__init__(Xpos, Ypos, yours)
        self._type1="vs"
        self.name="Patrick"
        self._picture=pygame.image.load("pictures/patrick.png")
        self._cost=3
        self._original_defence=3
        self._original_attack=3
        self._defence=3
        self._attack=3

class Dhru(Fighter_card):
    def __init__(self, Xpos, Ypos, yours):
        super().__init__(Xpos, Ypos, yours)
        self._type1="vs"
        self.name="Dhru"
        self._picture=pygame.image.load("pictures/dhru.png")
        self._original_defence=5
        self._original_attack=8
        self._cost=6
        self._defence=5
        self._attack=8

class Doris(Fighter_card):
    def __init__(self, Xpos, Ypos, yours):
        super().__init__(Xpos, Ypos, yours)
        self._type1="vs"
        self.name="Doris"
        self._effect_text="Dodge: 3"
        self._picture=pygame.image.load("pictures/doris.png")
        self._original_defence=1
        self._original_attack=7
        self._cost=10
        self._defence=1
        self._attack=7
        self.dodge=3

class Dan(Fighter_card):
    def __init__(self, Xpos, Ypos, yours):
        super().__init__(Xpos, Ypos, yours)
        self._type1="vs"
        self.name="Dan"
        self._effect_text="Magic: Add 3 turtles to your hand, when a turtle is played gain 2 defence"
        self._picture=pygame.image.load("pictures/dan.png")
        self._original_defence=6
        self._original_attack=12
        self._cost=12
        self._defence=6
        self._attack=12
        self.splash=7

    def magic(self, card, current_player, other_player, board):
        current_player.gain_card("turtle")
        current_player.gain_card("turtle")
        current_player.gain_card("turtle")

#turtles
class Hungry(Fighter_card):
    def __init__(self, Xpos, Ypos, yours):
        super().__init__(Xpos, Ypos, yours)
        self.name="Hungry"
        self._type1="turtle"
        self._picture=pygame.image.load("pictures/hungry (human version).png")
        self._original_defence=6
        self._original_attack=12
        self._cost=7
        self._defence=6
        self._attack=12

    def magic(self, card, player1, player2, board):
        for i in range(0, 8):
            if isinstance(board.get_cards()[i], Dan):
                board.get_cards()[i].change_defence(2)

class Turtle(Fighter_card):
    def __init__(self, Xpos, Ypos, yours):
        super().__init__(Xpos, Ypos, yours)
        self.name="Turtle"
        self._type1="turtle"
        self._picture=pygame.image.load("pictures/turtle.png")
        self._original_defence=8
        self._original_attack=3
        self._cost=4
        self._defence=8
        self._attack=3

    def magic(self, card, player1, player2, board):
        for i in range(0, 8):
            if isinstance(board.get_cards()[i], Dan):
                board.get_cards()[i].change_defence(2)

class Tiny(Fighter_card):
    def __init__(self, Xpos, Ypos, yours):
        super().__init__(Xpos, Ypos, yours)
        self.name="Tiny"
        self._type1="turtle"
        self._picture=pygame.image.load("pictures/tiny.png")
        self._original_defence=6
        self._original_attack=1
        self._cost=2
        self._defence=6
        self._attack=1

    def magic(self, card, player1, player2, board):
        for i in range(0, 8):
            if isinstance(board.get_cards()[i], Dan):
                board.get_cards()[i].change_defence(2)

class Strongest_strong(Spell_card):
    def __init__(self, Xpos, Ypos, yours):
        super().__init__(Xpos, Ypos, yours)
        self._type1="vs"
        self.name="Strongest strong"
        self._effect_text="Give a card +6 attack"
        self._picture=pygame.image.load("pictures/strongest strong.png")
        self._cost=3

    def magic_test(self):
        return True

    def magic(self, card, player1, player2, board):
        card.change_attack(6)

class He_eat_snac(Spell_card):
    def __init__(self, Xpos, Ypos, yours):
        super().__init__(Xpos, Ypos, yours)
        self._type1="vs"
        self.name="He eat snac"
        self._effect_text="Give a card +6 defence"
        self._picture=pygame.image.load("pictures/he eat snac.png")
        self._cost=3

    def magic_test(self):
        return True

    def magic(self, card, player1, player2, board):
        card.change_defence(6)

#guide to making cards:
#
#copy one of the codes above
#inherit from Spell_card or Fighter_card depending on which you want
#set self.name to its name
#set self._cost, self._attack and self._defence to your prefrence
#you will also need to set self._original_attack and
#self._original_defence to the same thing
#if you dont want it to be vs type set self._type1 to something else
#to give taunt set self.taunt to True
#to give thorns set self.thorns to True
#to give haste set self.paralysis to 0
#to give transparency set self.transparency to True
#to give annoying set self.annoying to True
#to give dodge set self.original_dodge to the number you want
#to give splash set self.splash to the attack you want
#
#effects:
#to make it paralise something, make it ADD 1 to the paralysis value
#of the other card for each turn of paralysis
#
#to give an imunity to silence rewrite
#the silence function for that card to nothing
#
#to add a magic effect redefine the magic function to what you want

def get_total_cards():
                #regular cards
    total_cards=[Patrick(-200, -200, True),\
                 Dhru(-200, -200, True),\
                 Doris(-200, -200, True),\
                 Dan(-200, -200, True),\
                 #turtles
                 Hungry(-200, -200, True),\
                 Turtle(-200, -200, True),\
                 Tiny(-200, -200, True),\
                 #spells
                 Strongest_strong(-200, -200, True),\
                 He_eat_snac(-200, -200, True)]
    return total_cards
