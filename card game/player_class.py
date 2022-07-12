import card_class
import random

class Player:
    def __init__(self):
        self._player_cards=[]
        self._money=0
        self._lives=5
        self._name=None

    def get_money(self):
        return self._money

    def get_lives(self):
        return self._lives

    def get_name(self):
        return self._name

    def change_name(self, new_name):
        self._name=new_name

    def add_lives(self, amount):
        self._lives+=amount

    def add_money(self, amount):
        self._money+=amount

    def gain_card(self, type1):
        possible_cards=card_class.get_total_cards()
        possible=False
        while not possible:
            ran=random.randint(0, len(possible_cards)-1)
            if possible_cards[ran].get_type1()==type1:
                possible=True
        self._player_cards.append(possible_cards[ran])
