import pygame
import Assets.Scripts.map as maps
import Assets.Scripts.framework as engine


pygame.init()

from pygame.locals import *

s_width = 800
s_height = 500
screen = pygame.display.set_mode((s_width, s_height))
display = pygame.Surface((s_width//2, s_height//2))


def get_image(sheet, frame, width, height, scale, colorkey, scale_coordinates = []):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    if scale_coordinates == []:
        image = pygame.transform.scale(image, (width * scale, height * scale))
    else:
        image = pygame.transform.scale(image, scale_coordinates )
    image.set_colorkey(colorkey)
    return image


#Loading images
squirrel_idle_spritesheet = pygame.image.load("./Assets/Sprites/squirrel_idle.png").convert_alpha()
squirrel_run_spritesheet = pygame.image.load("./Assets/Sprites/squirrel_run.png").convert_alpha()


squirrel_idle_animation = []
squrrel_run_animation = []
for x in range(4):
    squirrel_idle_animation.append(get_image(squirrel_idle_spritesheet, x, 25, 24, 1.5, (63, 72, 204)))
    squrrel_run_animation.append(get_image(squirrel_run_spritesheet, x, 30, 18, 1.5, (63, 72, 204), [25*1.5,24*1.5]))


map = maps.Map("./Assets/Maps/map.txt", 32, "./Assets/Tiles", True, True)
tile_rects = map.get_rect()
player = engine.Player(50,50, squirrel_idle_animation[0].get_width(), squirrel_idle_animation[1].get_height(), squirrel_idle_animation, squrrel_run_animation)
true_scroll = [0,0]
run = True

clock = pygame.time.Clock()

while run:
    clock.tick(60)
    time = pygame.time.get_ticks()
    display.fill((50,50,0))

    true_scroll[0] += (player.get_rect().x - true_scroll[0] - 202) / 5
    true_scroll[1] += (player.get_rect().y - true_scroll[1] - 132) / 5
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    map.draw(display, scroll)

    player.move(tile_rects, time)
    player.draw(display, scroll)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    surf = pygame.transform.scale(display, (s_width, s_height))
    screen.blit(surf, (0,0))
    
    pygame.display.flip()