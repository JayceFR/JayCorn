import pygame
import Assets.Scripts.map as maps
import Assets.Scripts.framework as engine


pygame.init()

from pygame.locals import *

s_width = 800
s_height = 500
screen = pygame.display.set_mode((s_width, s_height))
display = pygame.Surface((s_width//2, s_height//2))

map = maps.Map("./Assets/Maps/map.txt", 32, "./Assets/Tiles", True, True)
tile_rects = map.get_rect()
player = engine.Player(50,50, 32, 32)
true_scroll = [0,0]
run = True

while run:
    display.fill((0,0,0))

    true_scroll[0] += (player.get_rect().x - true_scroll[0] - 202) / 5
    true_scroll[1] += (player.get_rect().y - true_scroll[1] - 132) / 5
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    map.draw(display, scroll)

    player.move(tile_rects)
    player.draw(display, scroll)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    surf = pygame.transform.scale(display, (s_width, s_height))
    screen.blit(surf, (0,0))
    
    pygame.display.flip()