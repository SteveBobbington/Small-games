import pygame
import os, sys
import card_class, button_class, player_class, interface_class


def get_name(interface, player, no):
    name="Player"
    quit_button=button_class.Button((20, 20, 100, 50), button_class.button_quit, "Quit")
    player_box, player_box_rect=interface.add_box((550, 200, 200, 60))
    player_text, player_text_rect=interface.add_text((player_box_rect[0]+20, player_box_rect[1]+10, 160, 40), "Enter player %s name" % no)
    input_box, input_box_rect=interface.add_box((400, 300, 500, 60))
    text=""
    while name=="Player":
        for event in pygame.event.get():
            quit_button.is_pressed()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    name=text
                if event.key==pygame.K_BACKSPACE:
                    text=text[:-1]
                else:
                    text+=event.unicode
        interface.screen.fill((0, 0, 0))
        text_surface, text_surface_rect=interface.add_text((input_box_rect[0]+15, input_box_rect[1]+10, (23*len(text) if len(text)<=19 else 460), 40), text)
        quit_button.draw(interface.screen)
        interface.screen.blit(player_box, player_box_rect)
        interface.screen.blit(player_text, player_text_rect)
        interface.screen.blit(input_box, input_box_rect)
        interface.screen.blit(text_surface, text_surface_rect)
        pygame.display.update()
    player.change_name(name)

def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "50, 50"
    pygame.init()
    screenSize=[1300, 650]
    screen=pygame.display.set_mode(screenSize)

    clock=pygame.time.Clock()

    player1=player_class.Player()
    player2=player_class.Player()

    interface=interface_class.Interface(screen, player1, player2)

    get_name(interface, player1, 1)
    get_name(interface, player2, 2)

    running=True

    while running:
        if interface.bad_ticks==0:
            interface.get_events()
            interface.draw_screen()
            pygame.display.update()
        else:
            interface.bad_ticks-=1
        clock.tick(30)

if __name__=="__main__":
    main()
