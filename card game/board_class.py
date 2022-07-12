import pygame
import card_class

class Board:
    def __init__(self):
        self._cards=[]
        self.add_empty()

    def get_cards(self):
        return self._cards

    def add_spell(self, card):
        self._cards[8]=card

    def swap_cards(self):
        new_board=[]
        for i in range(4, 8):
            new_board.append(self._cards[i])
        for i in range(0, 4):
            new_board.append(self._cards[i])
        new_board.append(self._cards[9])
        new_board.append(self._cards[8])
        self._cards=[]
        X=410
        Y=50
        for i in range(0, 8):
            new_board[i].change_yours()
            new_board[i].change_pos(X, Y)
            self._cards.append(new_board[i])
            X+=120
            if i==3:
                X=410
                Y+=180
        new_board[8].change_yours()
        new_board[9].change_yours()
        new_board[8].change_pos(280, 180)
        new_board[9].change_pos(900, 100)
        self._cards.append(new_board[8])
        self._cards.append(new_board[9])

    def check_if_cards_played(self):
        played=False
        for i in range(4, 8):
            if not isinstance(self._cards[i], card_class.Empty):
                played=True
        return played

    def check_if_taunt(self):
        for i in range(0, 4):
            if self._cards[i].taunt==True:
                return True
        return False

    def add_card(self, card):
        listValue=card.get_rect()[0]
        listValue-=410
        listValue/=120
        listValue+=4
        del self._cards[int(listValue)]
        self._cards.insert(int(listValue), card)

    def kill_card(self, card):
        X=card.get_rect()[0]
        Y=card.get_rect()[1]
        X1=X
        X1-=410
        X1/=120
        if card.get_yours==True:
            X1+=4
        del self._cards[int(X1)]
        self._cards.insert(int(X1), card_class.Empty(X, Y, False))

    def add_empty(self):
        X=410
        Y=50
        yours=False
        for i in range(0, 8):
            self._cards.append(card_class.Empty(X, Y, yours))
            X+=120
            if i==3:
                yours=True
                X=410
                Y+=180
        self._cards.append(card_class.Spell_slot(280, 180, True))
        self._cards.append(card_class.Spell_slot(900, 100, False))

    def draw_cards(self, screen):
        for card in self._cards:
            card.draw(screen)
