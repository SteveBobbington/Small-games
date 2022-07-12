import pygame
import player_class, board_class, button_class, card_class
import time

class Interface:
    def __init__(self, screen, player1, player2):
        self.player1=player1
        self.player2=player2
        self.board=board_class.Board()
        self.screen=screen
        self.current_player=self.player1
        self.font=pygame.font.SysFont("DTM-Mono", 72)
        self._users_cards=[]
        self.buttons_to_draw=[]
        self.texts_to_draw=[]
        self.text_rects_to_draw=[]
        self.boxes_to_draw=[]
        self.box_rects_to_draw=[]
        self.bad_ticks=0
        self.picking=False
        self.spell_picking=False
        self.attacking=False
        self.magic_picking=False
        self.empty_image=pygame.image.load("pictures/empty.png")
        self.turn=1
        self.current_player._money+=1
        self.current_player.gain_card("vs")
        self.winner=None
        self.add_buttons()

    def draw_player_cards(self):
        X=20
        Y=450
        for card in self._users_cards:
            card.change_pos(X, Y)
            card.draw(self.screen)
            X+=130

    def draw_boxes(self):
        for i in range(0, len(self.boxes_to_draw)):
            self.screen.blit(self.boxes_to_draw[i], self.box_rects_to_draw[i])

    def draw_texts(self):
        for i in range(0, len(self.texts_to_draw)):
            self.screen.blit(self.texts_to_draw[i], self.text_rects_to_draw[i])

    def add_box(self, rect):
        rect=pygame.Rect(rect)
        image=pygame.transform.scale(self.empty_image, (rect[2], rect[3]))
        return image, rect

    def add_text(self, rect, text):
        text=self.font.render(text, True, pygame.Color("white"))
        text_rect=pygame.Rect(rect)
        text=pygame.transform.scale(text, (rect[2], rect[3]))
        return text, rect

    def unpick(self):
        self.boxes_to_draw.remove(self.pick_image)
        self.box_rects_to_draw.remove(self.pick_rect)
        self.texts_to_draw.remove(self.pick_text)
        self.text_rects_to_draw.remove(self.pick_text_rect)
        self.buttons_to_draw.remove(self.back_button)
        self.picking=False
        self.spell_picking=False
        try:
            try:
                self.boxes_to_draw.remove(self.expensive)
                self.box_rects_to_draw.remove(self.expensive_rect)
                self.texts_to_draw.remove(self.expensive_text)
                self.text_rects_to_draw.remove(self.expensive_text_rect)
            except AttributeError:
                pass
        except ValueError:
            pass

    def unattack(self):
        self.boxes_to_draw.remove(self.attack_image)
        self.box_rects_to_draw.remove(self.attack_rect)
        self.texts_to_draw.remove(self.attack_text)
        self.text_rects_to_draw.remove(self.attack_text_rect)
        self.buttons_to_draw.remove(self.back_button)
        self.attacking=False

    def create_stats(self):
        try:
            self.boxes_to_draw.remove(self.stats_image)
            self.box_rects_to_draw.remove(self.stats_rect)
            self.texts_to_draw.remove(self.stats_text1)
            self.text_rects_to_draw.remove(self.stats_text_rect1)
            self.texts_to_draw.remove(self.stats_text2)
            self.text_rects_to_draw.remove(self.stats_text_rect2)
            self.texts_to_draw.remove(self.stats_text3)
            self.text_rects_to_draw.remove(self.stats_text_rect3)
            self.texts_to_draw.remove(self.stats_text4)
            self.text_rects_to_draw.remove(self.stats_text_rect4)
        except AttributeError:
            pass
        self.stats_image, self.stats_rect=self.add_box((1150, 10, 120, 105))
        self.stats_text1, self.stats_text_rect1=self.add_text((self.stats_rect[0]+10, self.stats_rect[1]+5, 70, 20), "%s Stats" % self.current_player.get_name())
        self.stats_text2, self.stats_text_rect2=self.add_text((self.stats_rect[0]+10, self.stats_rect[1]+30, 90, 20), "Money: "+str(self.current_player.get_money()))
        self.stats_text3, self.stats_text_rect3=self.add_text((self.stats_rect[0]+10, self.stats_rect[1]+55, 70, 20), "Turn: "+str(self.turn))
        self.stats_text4, self.stats_text_rect4=self.add_text((self.stats_rect[0]+10, self.stats_rect[1]+80, 90, 20), "Lives: "+str(self.current_player.get_lives()))
        self.boxes_to_draw.append(self.stats_image)
        self.box_rects_to_draw.append(self.stats_rect)
        self.texts_to_draw.append(self.stats_text1)
        self.text_rects_to_draw.append(self.stats_text_rect1)
        self.texts_to_draw.append(self.stats_text2)
        self.text_rects_to_draw.append(self.stats_text_rect2)
        self.texts_to_draw.append(self.stats_text3)
        self.text_rects_to_draw.append(self.stats_text_rect3)
        self.texts_to_draw.append(self.stats_text4)
        self.text_rects_to_draw.append(self.stats_text_rect4)
        
    def add_buttons(self):
        self.end_turn_button=button_class.Button((1180, 335, 100, 50), self.end_turn, "End turn")
        self.quit_button=button_class.Button((20, 20, 100, 50), button_class.button_quit, "Quit")
        self.buttons_to_draw.append(self.end_turn_button)
        self.buttons_to_draw.append(self.quit_button)

    def draw_screen(self):
        self.create_stats()
        self.screen.fill((0, 0, 0))
        print(self.boxes_to_draw)
        if self.winner==self.player1:
            self.quit_button.draw(self.screen)
            self.won_box, self.won_box_rect=self.add_box((250, 225, 800, 200))
            self.won_text, self.won_text_rect=self.add_text((self.won_box_rect[0]+50, self.won_box_rect[1]+20, 700, 160), "%s has WON!" % self.player1.get_name())
            self.screen.blit(self.won_box, self.won_box_rect)
            self.screen.blit(self.won_text, self.won_text_rect)
        elif self.winner==self.player2:
            self.quit_button.draw(self.screen)
            self.won_box, self.won_box_rect=self.add_box((400, 225, 500, 200))
            self.won_text, self.won_text_rect=self.add_text((self.won_box_rect[0]+50, self.won_box_rect[1]+20, 400, 160), "%s has WON!" % self.player2.get_name())
            self.screen.blit(self.won_box, self.won_box_rect)
            self.screen.blit(self.won_text, self.won_text_rect)
        else:
            self.board.draw_cards(self.screen)
            button_class.draw_buttons(self.buttons_to_draw, self.screen)
            self.draw_boxes()
            self.draw_texts()
            self._users_cards=self.current_player._player_cards
            self.draw_player_cards()

    def get_events(self):
        for event in pygame.event.get():
            for button in self.buttons_to_draw:
                button.is_pressed()
            for card in self._users_cards:
                #in users hand
                if card.is_pressed():
                    if self.picking:
                        #when picking new fighter
                        if card._type2=="fighter":
                            #is a fighter
                            if self.current_player.get_money()>=card.get_cost():
                                #can afford
                                card.change_pos(self.place.get_rect()[0], self.place.get_rect()[1])
                                self.board.add_card(card)
                                self._users_cards.remove(card)
                                self.unpick()
                                self.current_player.add_money(-card.get_cost())
                                if not card.magic_test():
                                    if self.current_player==self.player1:
                                        other_player=self.player2
                                    else:
                                        other_player=self.player1
                                    card.magic(card, self.current_player, other_player, self.board)
                                else:
                                    self.magic_card=card
                                    self.magic_picking=True
                            else:
                                #cant afford
                                self.expensive, self.expensive_rect=self.add_box((20, 200, 250, 50))
                                self.expensive_text, self.expensive_text_rect=self.add_text((self.expensive_rect[0]+10, self.expensive_rect[1]+5, 200, 40), "You can't afford that")
                                self.boxes_to_draw.append(self.expensive)
                                self.box_rects_to_draw.append(self.expensive_rect)
                                self.texts_to_draw.append(self.expensive_text)
                                self.text_rects_to_draw.append(self.expensive_text_rect)
                    elif self.spell_picking:
                        #when picking new spell
                        if card._type2=="spell":
                            #is a spell
                            if self.current_player.get_money()>=card.get_cost():
                                #can afford
                                card.change_pos(self.place.get_rect()[0], self.place.get_rect()[1])
                                self.board.add_spell(card)
                                self._users_cards.remove(card)
                                self.unpick()
                                self.current_player.add_money(-card.get_cost())
                                if not card.magic_test():
                                    if self.current_player==self.player1:
                                        other_player=self.player2
                                    else:
                                        other_player=self.player1
                                    card.magic(card, self.current_player, other_player, self.board)
                                    time.sleep(1)
                                    self.board.add_spell(card_class.Spell_slot(card.get_rect()[0], card.get_rect()[1], True))
                                else:
                                    self.magic_card=card
                                    self.magic_picking=True
                            else:
                                #cant afford
                                self.expensive, self.expensive_rect=self.add_box((20, 200, 250, 50))
                                self.expensive_text, self.expensive_text_rect=self.add_text((self.expensive_rect[0]+10, self.expensive_rect[1]+5, 200, 40), "You can't afford that")
                                self.boxes_to_draw.append(self.expensive)
                                self.box_rects_to_draw.append(self.expensive_rect)
                                self.texts_to_draw.append(self.expensive_text)
                                self.text_rects_to_draw.append(self.expensive_text_rect)
            for card in self.board._cards:
            #is on the board
                if card.is_pressed():
                    if self.magic_picking==True:
                        if self.current_player==self.player1:
                            other_player=self.player2
                        else:
                            other_player=self.player1
                        self.magic_card.magic(card, self.current_player, other_player, self.board)
                        time.sleep(1)
                        self.board.add_spell(card_class.Spell_slot(self.board.get_cards()[8].get_rect()[0], self.board.get_cards()[8].get_rect()[1], True))
                        self.magic_picking=False
                    elif card.get_yours():
                        #is on your side
                        if isinstance(card, card_class.Empty):
                            #is an empty space
                            time.sleep(0.1)
                            self.picking=True
                            self.back_button=button_class.Button((20, 330, 100, 50), self.unpick, "Back")
                            self.buttons_to_draw.append(self.back_button)
                            self.pick_image, self.pick_rect=self.add_box((20, 250, 250, 50))
                            self.boxes_to_draw.append(self.pick_image)
                            self.box_rects_to_draw.append(self.pick_rect)
                            self.pick_text, self.pick_text_rect=self.add_text((self.pick_rect[0]+10, self.pick_rect[1]+5, 200, 40), "Pick a card to place")
                            self.texts_to_draw.append(self.pick_text)
                            self.text_rects_to_draw.append(self.pick_text_rect)
                            self.place=card
                        elif isinstance(card, card_class.Spell_slot):
                            #is an empty spell space
                            time.sleep(0.1)
                            self.spell_picking=True
                            self.back_button=button_class.Button((20, 330, 100, 50), self.unpick, "Back")
                            self.buttons_to_draw.append(self.back_button)
                            self.pick_image, self.pick_rect=self.add_box((20, 250, 250, 50))
                            self.boxes_to_draw.append(self.pick_image)
                            self.box_rects_to_draw.append(self.pick_rect)
                            self.pick_text, self.pick_text_rect=self.add_text((self.pick_rect[0]+10, self.pick_rect[1]+5, 200, 40), "Pick a card to place")
                            self.texts_to_draw.append(self.pick_text)
                            self.text_rects_to_draw.append(self.pick_text_rect)
                            self.place=card
                        elif card.get_type2()=="fighter":
                            #is a fighter
                            if self.attacking==True:
                                if card.paralysis==0:
                                    #if card youre attacking with isnt paralised
                                    for i in range(0, 4):
                                        if self.board.get_cards()[i]==self.target:
                                            adjacent1=self.board.get_cards()[i-1]
                                            adjacent2=self.board.get_cards()[i+1]
                                    if card.splash>adjacent1.get_defence():
                                        self.board.kill_card(adjacent1)
                                    if card.splash>adjacent2.get_defence():
                                        self.board.kill_card(adjacent2)
                                    if self.target.thorns==True or card.annoying==True:
                                        #if target has thorns
                                        if self.target.get_attack>card.get_defence():
                                            self.board.kill_card(card)
                                    if self.target.dodge>0 and card.get_attack()>0:
                                        self.target.dodge-=1
                                    elif card.get_attack()>self.target.get_defence():
                                        self.board.kill_card(self.target)
                                card.transparency=False
                                self.unattack()
                    else:
                        #is on the enemies side
                        if card.get_type2()=="fighter":
                            #is a fighter
                            if card.transparency==False:
                                if not self.board.check_if_taunt():
                                    #there are no taunts
                                    self.attacking=True
                                    self.back_button=button_class.Button((20, 330, 100, 50), self.unattack, "Back")
                                    self.buttons_to_draw.append(self.back_button)
                                    self.attack_image, self.attack_rect=self.add_box((20, 250, 250, 50))
                                    self.boxes_to_draw.append(self.attack_image)
                                    self.box_rects_to_draw.append(self.attack_rect)
                                    self.attack_text, self.attack_text_rect=self.add_text((self.attack_rect[0]+10, self.attack_rect[1]+5, 200, 40), "Pick a card to attack with")
                                    self.texts_to_draw.append(self.attack_text)
                                    self.text_rects_to_draw.append(self.attack_text_rect)
                                    self.target=card
                                elif card.taunt=="True":
                                    #this card is a taunt
                                    self.attacking=True
                                    self.back_button=button_class.Button((20, 330, 100, 50), self.unattack, "Back")
                                    self.buttons_to_draw.append(self.back_button)
                                    self.attack_image, self.attack_rect=self.add_box((20, 250, 250, 50))
                                    self.boxes_to_draw.append(self.attack_image)
                                    self.box_rects_to_draw.append(self.attack_rect)
                                    self.attack_text, self.attack_text_rect=self.add_text((self.attack_rect[0]+10, self.attack_rect[1]+5, 200, 40), "Pick a card to attack with")
                                    self.texts_to_draw.append(self.attack_text)
                                    self.text_rects_to_draw.append(self.attack_text_rect)
                                    self.target=card

    def end_turn(self):
        #end of turn things:
        self.bad_ticks+=5
        if self.current_player==self.player1:
            self.current_player=self.player2
            self.turn+=1
        else:
            self.current_player=self.player1
        if self.turn<8:
            self.current_player._money+=self.turn
        else:
            self.current_player._money+=8
        self.current_player.gain_card("vs")
        self.board.swap_cards()
        #start of turn things:
        #every turn removes 1 paralysis
        for i in range(4, 8):
            self.board.get_cards()[i].paralysis-=1
        #resets dodges
        for i in range(4, 8):
            self.board.get_cards()[i].dodge=self.board.get_cards()[i].original_dodge
        if self.turn>4 and not self.board.check_if_cards_played():
            self.current_player.add_lives(-1)
        if self.current_player.get_lives()<=0:
            if self.current_player==self.player1:
                self.winner=self.player2
            else:
                self.winner=self.player1
