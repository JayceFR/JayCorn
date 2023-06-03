import pygame
import math, random
import Assets.Scripts.map as maps
import Assets.Scripts.framework as engine
import Assets.Scripts.bg_particles as bg_particles
import Assets.Scripts.bird as bird
import Assets.Scripts.fireflies as fireflies
import Assets.Scripts.grass as g
import Assets.Scripts.acorn as jaycorn
import Assets.Scripts.chuma as chuma
import Assets.Scripts.sparks as spark
import Assets.Scripts.typewriter as typewriter
import Assets.Scripts.shader as shader
import time as t


pygame.init()

from pygame.locals import *

s_width = 800
s_height = 500
window = pygame.display.set_mode((s_width, s_height), pygame.OPENGL | pygame.DOUBLEBUF)
screen = pygame.Surface((s_width, s_height))
display = pygame.Surface((s_width//2, s_height//2))
ui_display = pygame.Surface((s_width//2, s_height//2), pygame.SRCALPHA)
pygame.display.set_caption("JayCorn")


def get_image(sheet, frame, width, height, scale, colorkey, scale_coordinates = []):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    if scale_coordinates == []:
        image = pygame.transform.scale(image, (width * scale, height * scale))
    else:
        image = pygame.transform.scale(image, scale_coordinates )
    image.set_colorkey(colorkey)
    return image

def blit_grass(grasses, display, scroll, player):
    for grass in grasses:
        if grass.get_rect().colliderect(player.get_rect()):
            grass.colliding()
        grass.draw(display, scroll)

def draw_text(text, font, text_col, x, y, display):
    img = font.render(text, True, text_col)
    display.blit(img, (x, y))


#Loading images
squirrel_idle_spritesheet = pygame.image.load("./Assets/Sprites/squirrel_idle.png").convert_alpha()
squirrel_run_spritesheet = pygame.image.load("./Assets/Sprites/squirrel_run.png").convert_alpha()
leaf_img = pygame.image.load("./Assets/Entities/leaf.png").convert_alpha()
leaf_img.set_colorkey((0,0,0))
leaf_img2 = pygame.image.load("./Assets/Entities/leaf2.png").convert_alpha()
leaf_img2.set_colorkey((0,0,0))
tree_img = pygame.image.load("./Assets/Entities/tree.png").convert_alpha()
tree_img = pygame.transform.scale(tree_img, (tree_img.get_width()*1.5, tree_img.get_height()*1.5))
tree_img.set_colorkey((0,0,0))
tree_img2 = pygame.image.load("./Assets/Entities/tree2.png").convert_alpha()
tree_img2 = pygame.transform.scale(tree_img2, (tree_img2.get_width()*1.5, tree_img2.get_height()*1.5))
tree_img2.set_colorkey((0,0,0))
bird_img = pygame.image.load("./Assets/Sprites/bird_fly.png").convert_alpha()
squirrel_jump = pygame.image.load("./Assets/Sprites/squirrel_jump.png").convert_alpha()
squirrel_jump = pygame.transform.scale(squirrel_jump, (25*1.5,24*1.5))
squirrel_fall = squirrel_jump.copy()
squirrel_jump = pygame.transform.rotate(squirrel_jump, 45)
squirrel_jump.set_colorkey((63,72,204))
squirrel_fall = pygame.transform.rotate(squirrel_fall, -25)
squirrel_fall.set_colorkey((63,72,204))
acorn_idle_spritesheet = pygame.image.load("./Assets/Entities/acorn_idle.png").convert_alpha()
acorn_img = pygame.image.load("./Assets/Entities/acorn.png").convert_alpha()
acorn_logo_img = acorn_img.copy()
acorn_logo_img = pygame.transform.scale(acorn_logo_img, (acorn_img.get_width()*2, acorn_img.get_height()*2))
acorn_img = pygame.transform.scale(acorn_img, (acorn_img.get_width()*5, acorn_img.get_height()*5))
acorn_logo_img.set_colorkey((0,0,0))
acorn_img.set_colorkey((0,0,0))    
left_click_img = pygame.image.load("./Assets/Entities/left_click.png").convert_alpha()
left_click_img = pygame.transform.scale(left_click_img, (left_click_img.get_width()*2, left_click_img.get_height()*2))
left_click_img.set_colorkey((255,255,255))
left_click_ani_spritesheet = pygame.image.load("./Assets/Entities/left_click_ani.png").convert_alpha()
map1_img = pygame.image.load("./Assets/Entities/map1.png").convert_alpha()
map1_img = pygame.transform.scale(map1_img, (map1_img.get_width()*4, map1_img.get_height()*4))
map1_img.set_colorkey((255,255,255))
map2_img = pygame.image.load("./Assets/Entities/map2.png").convert_alpha()
map2_img = pygame.transform.scale(map2_img, (map2_img.get_width()*4, map2_img.get_height()*4))
map2_img.set_colorkey((255,255,255))
map3_img = pygame.image.load("./Assets/Entities/map3.png").convert_alpha()
map3_img = pygame.transform.scale(map3_img, (map3_img.get_width()*4, map3_img.get_height()*4))
map3_img.set_colorkey((255,255,255))
map4_img = pygame.image.load("./Assets/Entities/map4.png").convert_alpha()
map4_img = pygame.transform.scale(map4_img, (map4_img.get_width()*4, map4_img.get_height()*4))
map4_img.set_colorkey((255,255,255))
map5_img = pygame.image.load("./Assets/Entities/map5.png").convert_alpha()
map5_img = pygame.transform.scale(map5_img, (map5_img.get_width()*4, map5_img.get_height()*4))
map5_img.set_colorkey((255,255,255))
map1_ani_spritesheet = pygame.image.load("./Assets/Entities/map1_ani.png").convert_alpha()
map2_ani_spritesheet = pygame.image.load("./Assets/Entities/map2_ani.png").convert_alpha()
map3_ani_spritesheet = pygame.image.load("./Assets/Entities/map3_ani.png").convert_alpha()
map4_ani_spritesheet = pygame.image.load("./Assets/Entities/map4_ani.png").convert_alpha()
map5_ani_spritesheet = pygame.image.load("./Assets/Entities/map5_ani.png").convert_alpha()
jump_spark_img = pygame.image.load("./Assets/Entities/jump_spark.png").convert_alpha()
background_img = pygame.image.load("./Assets/Entities/background.png").convert_alpha()
background_img = pygame.transform.scale(background_img, (background_img.get_width()*2, background_img.get_height()*3))
fence_img = pygame.image.load("./Assets/Entities/fence.png").convert_alpha()
fence_img = pygame.transform.scale(fence_img, (32, 19))
fence_img.set_colorkey((255,255,255))
house_img = pygame.image.load("./Assets/Entities/housy.png").convert_alpha()
house_img = pygame.transform.scale(house_img, (house_img.get_width()*2, house_img.get_height()*2))
house_img.set_colorkey((255,255,255))
squirrel_head = pygame.image.load("./Assets/Entities/squirrel_head.png").convert_alpha()
squirrel_head = pygame.transform.scale(squirrel_head, (squirrel_head.get_width()*4, squirrel_head.get_height()*4))
squirrel_head.set_colorkey((63, 72, 204))
leaf_imgs = [leaf_img, leaf_img2]

squirrel_idle_animation = []
squrrel_run_animation = []
bird_animation = []
acorn_idle_animation = []
left_click_animation = []
jump_spark_animation = []
map1_ani = []
map2_ani = []
map3_ani = []
map4_ani = []
map5_ani = []
for x in range(4):
    squirrel_idle_animation.append(get_image(squirrel_idle_spritesheet, x, 25, 24, 1.5, (63, 72, 204)))
    squrrel_run_animation.append(get_image(squirrel_run_spritesheet, x, 30, 18, 1.5, (63, 72, 204), [25*1.5,24*1.5]))
    bird_animation.append(get_image(bird_img, x, 22, 14, 2, (69,40,60)))
    acorn_idle_animation.append(get_image(acorn_idle_spritesheet, x, 11, 12, 1.5, (0,0,0)))
    left_click_animation.append(get_image(left_click_ani_spritesheet, x, 6, 11, 4, (255,255,255)))
    jump_spark_animation.append(get_image(jump_spark_img, x, 32, 32, 1, (0,0,0)))
    map1_ani.append(get_image(map1_ani_spritesheet, x, 96, 59, 4, (255,255,255)))
    map2_ani.append(get_image(map2_ani_spritesheet, x, 96, 59, 4, (255,255,255)))
    map3_ani.append(get_image(map3_ani_spritesheet, x, 96, 59, 4, (255,255,255)))
    map4_ani.append(get_image(map4_ani_spritesheet, x, 96, 59, 4, (255,255,255)))
    map5_ani.append(get_image(map5_ani_spritesheet, x, 96, 59, 4, (255,255,255)))


map = maps.Map("./Assets/Maps/map.txt", 32, "./Assets/Tiles", True, True, {"o": [], "p" : [], "b" : [], "s" : [], "g" : [], "a" : [], "f" : [], "h" : []})
tile_rects, entity_loc = map.get_rect()
player = engine.Player(entity_loc['s'][0][0],entity_loc['s'][0][1], squirrel_idle_animation[0].get_width(), squirrel_idle_animation[1].get_height(), squirrel_idle_animation, squrrel_run_animation, squirrel_jump, squirrel_fall)
true_scroll = [0,0]
run = True

birdies = []
if len(entity_loc['b']) != 0:
    for loc in entity_loc['b']:
        birdies.append(bird.Bird(loc[0], loc[1], 32, 32, bird_animation))

acorns = []
#final_destination = [[(996,360), map1_img, False], [(2299,838), map2_img, False], [(1335,360), map3_img, False] , [(1932,582), map4_img, False], [(2599,198), map5_img, False]]
if len(entity_loc['a']) != 0:
    for pos, loc in enumerate(entity_loc['a']):
        acorns.append(jaycorn.Acorn(loc[0], loc[1], acorn_idle_animation[0].get_width(), acorn_idle_animation[0].get_height(), acorn_idle_animation, pos))


clock = pygame.time.Clock()
bg_particle_effect = bg_particles.Master(leaf_imgs)
firefly = fireflies.Fireflies(0, 100, 3000, 1000)

#Grass
grasses = []
for loc in entity_loc['g']:
    x_pos = loc[0]
    while x_pos < loc[0] + 32:
        x_pos += 2.5
        grasses.append(g.grass([x_pos, loc[1]+(14*2)], 2, 9))
grass_loc = []
grass_last_update = 0
grass_cooldown = 50

#Chuma stuff
left_click = chuma.Chuma(left_click_animation)
jump_spark = chuma.Chuma(jump_spark_animation)
map_1 = chuma.Chuma(map1_ani, False, 100)
map_2 = chuma.Chuma(map2_ani, False, 100)
map_3 = chuma.Chuma(map3_ani, False, 100)
map_4 = chuma.Chuma(map4_ani, False, 100)
map_5 = chuma.Chuma(map5_ani, False, 100)
show_jump_ani = [False, (0,0)]
show_jump_ani_last_update = 0
show_jump_ani_cooldown = 600
click = False

#Shader stuff
shader_obj = shader.Shader(True, "./Assets/Shader/vertex.vert", "./Assets/Shader/fragment.frag")
noise_img = pygame.image.load("./Assets/Shader/pnoise.png").convert_alpha()

#Typer seetings
font = pygame.font.Font("./Assets/Fonts/jayce.ttf", 18)
typer = typewriter.TypeWriter(font, (40,135,140), 40, 10, 400,9)
tutorial_typer = typewriter.TypeWriter(font, (0,19,127), 80, 180, 400, 9)
tutorial_typer.write(["Hi There", "I am Jay the squirrel", "As it is Autumn now, The next season is Winter", "Can you please help me...", "Find acorns and bury them into specific locations", "Beware of birds", "They may steal your Acorn", "Hide under trees to save your self"])
done_typing = False
done_tutorial = False

final_destination = [[(996,360), map_1, False], [(2299,838), map_2, False], [(1335,360), map_3, False] , [(1932,582), map_4, False], [(2599,198), map_5, False]]
acorns_buried = 0

game_over_highlights = ["The poor squirrel and his family perished in hunger during the cold and freezing winter ", "The squirrel and his family starved throughout the cold winter ", "The squirrel had to fast every week to survive the freezing cold winter", "The squirrel had enough acorns to survive the winter happily, but he didn't have any to provide to his starving family", "The squirrel and his entire family had enough acorns to survive the winter, but they needed to spend every morning with no food ", "The squirrel and his entire family rejoiced over the cold winter by eating acorns and playing games created by JayJan."]

#Inventory
has_acorn = False

safe = False

sparks = []
scroll = [0,0]

acorn_pos = -1

game_over = True

show_map = False

initialise_type_writer = True

start_time = t.time()
while run:
    clock.tick(60)
    time = pygame.time.get_ticks()
    display.fill((0,0,0))
    ui_display.fill((0,0,0,0))
    #print(clock.get_fps())
    draw_text(str(acorns_buried) + " / 5", font, (255,255,255), 325, 5, ui_display)
    ui_display.blit(acorn_logo_img, (370, 0))
    #print(player.get_rect().x, player.get_rect().y)
    game_over = True
    #Checking if game is over
    for destination in final_destination:
        if destination[2] == False:
            game_over = False
    if game_over:
        if initialise_type_writer:
            typer.write([game_over_highlights[acorns_buried]])
            initialise_type_writer = False
            print("Game over")
    #print(game_over)

    true_scroll[0] += (player.get_rect().x - true_scroll[0] - 202) 
    true_scroll[1] += (player.get_rect().y - true_scroll[1] - 132) 
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    display.blit(background_img, (-50-scroll[0], -50-scroll[1]))

    #Grass movement
    if time - grass_last_update > grass_cooldown:
        for grass in grasses:
            grass.move()
        grass_last_update = time

    map.draw(display, scroll)
    for loc in entity_loc['f']:
        display.blit(fence_img, (loc[0] - scroll[0], loc[1] + 12 - scroll[1]))
    

    safe = False
    #Drawing trees and checking if player is safe
    if len(entity_loc['o']) != 0:
        for loc in entity_loc['o']:
            if player.get_rect().collidepoint(loc[0], loc[1]):
                safe = True
            display.blit(tree_img2, (loc[0] - scroll[0] - 69, loc[1] - scroll[1] - 110))
    if len(entity_loc['p']) != 0:
        for loc in entity_loc['p']:
            if player.get_rect().collidepoint(loc[0], loc[1]):
                safe = True
            display.blit(tree_img, (loc[0] - scroll[0] - 69, loc[1] - scroll[1] - 110))
    
    for loc in entity_loc['h']:
        display.blit(house_img, (loc[0]  - scroll[0], loc[1] - 50 - scroll[1]))
    
    #Drawing birds
    for birdie in birdies:
        birdie.move(time,safe, player.get_rect().x, player.get_rect().y, has_acorn)
        birdie.draw(display, scroll)
        if has_acorn:
            if birdie.get_rect().colliderect(player.get_rect()):
                final_destination[acorn_pos][2] = True
                has_acorn = False
                for x in range(50):
                    sparks.append(spark.Spark([25 ,15], math.radians(random.randint(0,360)), random.randint(5,7), (random.randint(0,255),random.randint(0,255),random.randint(0,255)), 2, 1))
    
    if not game_over:
        player.move(tile_rects, time, done_tutorial)
    player.draw(display, scroll)

    
    for pos, acorn in sorted(enumerate(acorns), reverse=True):
        if not has_acorn:
            if player.get_rect().colliderect(acorn.get_rect()):
                left_click.draw(time, ui_display, [0,0], (350, 200))
                if click:
                    acorn_pos = acorn.get_id()
                    acorns.pop(pos)
                    has_acorn = True
        acorn.move(time, tile_rects)
        acorn.draw(display, scroll)
        

    blit_grass(grasses, display, scroll, player)

    if has_acorn:
        ui_display.blit(acorn_img, (0,0))
        if player.get_rect().collidepoint(final_destination[acorn_pos][0]):
            #Dig animation
            left_click.draw(time, ui_display, [0,0], (350, 200))
            if click:
                for x in range(50):
                    sparks.append(spark.Spark([final_destination[acorn_pos][0][0] - scroll[0], final_destination[acorn_pos][0][1] - scroll[1]], math.radians(random.randint(0,360)), random.randint(2,5), (random.randint(0,255),random.randint(0,255),random.randint(0,255)), 2, 1))
                final_destination[acorn_pos][2] = True
                acorns_buried += 1
                has_acorn = False
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not click:
                    click = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if click:
                    click = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if show_map:
                    show_map = False
                    final_destination[acorn_pos][1].reset_frame()
                else:
                    if has_acorn:
                        show_map = True
            if (event.key == pygame.K_SPACE or event.key == pygame.K_w) and player.jump_count > 0:
                show_jump_ani = [True, (player.get_rect().x + 15, player.get_rect().y + 23)]
                show_jump_ani_last_update = time
        
    if show_jump_ani[0] == True:
        jump_spark.draw(time, ui_display, scroll, show_jump_ani[1])
        if time - show_jump_ani_last_update > show_jump_ani_cooldown:
            jump_spark.reset_frame()
            show_jump_ani[0] = False
    
    bg_particle_effect.recursive_call(time, display, scroll, 1)
    firefly.recursive_call(time, display, scroll)

    for s in sparks:
        s.move(1)
        s.draw(ui_display)

    if show_map:
        if final_destination[acorn_pos][2] != True:
            #display.blit(final_destination[acorn_pos][1], (0,0))
            final_destination[acorn_pos][1].draw(time, ui_display, [0,0], (0,0))

    if not done_tutorial:
        surface = pygame.Surface((500, 100))
        pygame.draw.rect(surface, (80,80,80), pygame.rect.Rect(0,0,500,100))
        surface.set_colorkey((0,0,0))
        display.blit(surface, (0,180), special_flags=BLEND_RGB_ADD)
        ui_display.blit(squirrel_head, (0, 180))
        done_tutorial = tutorial_typer.update(time, ui_display, [350,230])

    if game_over:
        if not done_typing:
            surface = pygame.Surface((500, 100))
            pygame.draw.rect(surface, (255,255,255), pygame.rect.Rect(0,0,500,100))
            surface.set_colorkey((0,0,0))
            ui_display.blit(surface, (0,0), special_flags=BLEND_RGB_ADD)
            done_typing = typer.update(time, ui_display)

    surf = pygame.transform.scale(display, (s_width, s_height))
    screen.blit(surf, (0,0))

    shader_obj.draw({"tex" : screen, "noise_tex1": noise_img, "ui_tex" : ui_display}, { "itime": int((t.time() - start_time) * 100) })
    
    pygame.display.flip()