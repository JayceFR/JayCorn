import pygame
class Player():
    def __init__(self, x, y, width, height, idle_animation, run_animation) -> None:
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.movement = [0,0]
        self.display_x = 0
        self.display_y = 0
        self.moving_left = False
        self.moving_right = False
        self.collision_type = {}
        self.speed = 4
        self.display_x = 0
        self.display_y = 0
        self.idle_animation = idle_animation
        self.run_animation = run_animation
        self.frame = 0
        self.frame_last_update = 0
        self.frame_cooldown = 200
        self.facing_right = True

    def collision_test(self, tiles):
        hitlist = []
        for tile in tiles:
            if tile.touchable:
                if self.rect.colliderect(tile.get_rect()):
                    hitlist.append(tile)
        return hitlist
    
    def collision_checker(self, tiles):
        collision_types = {"top": [False, []], "bottom": [False, []], "right": [False, []], "left": [False, []]}
        self.rect.x += self.movement[0]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[0] > 0:
                self.rect.right = tile.get_rect().left
                collision_types["right"][0] = True
                collision_types["right"][1].append(tile)
            elif self.movement[0] < 0:
                self.rect.left = tile.get_rect().right
                collision_types["left"][0] = True
                collision_types["left"][1].append(tile)
        self.rect.y += self.movement[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[1] > 0:
                self.rect.bottom = tile.get_rect().top
                collision_types["bottom"][0] = True
                collision_types["bottom"][1].append(tile)
            if self.movement[1] < 0:
                self.rect.top = tile.get_rect().bottom
                collision_types["top"][0] = True
                collision_types['top'][1].append(tile)
        return collision_types
    
    def move(self, tiles, time):
        self.movement = [0, 0]

        if self.moving_right:
            self.facing_right = True
            self.movement[0] += self.speed
            self.moving_right = False
        if self.moving_left:
            self.facing_right = False
            self.movement[0] -= self.speed
            self.moving_left = False

        if time - self.frame_last_update > self.frame_cooldown:
            self.frame_last_update = time
            self.frame += 1
            if self.frame >= 4:
                self.frame = 0

        self.movement[1] += 8

        self.collision_type = self.collision_checker(tiles)


        key = pygame.key.get_pressed()
        if  key[pygame.K_a]:
            self.moving_left = True
        if key[pygame.K_d]:
            self.moving_right = True
    
    def draw(self, display, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        if self.moving_right:
            display.blit(self.run_animation[self.frame], self.rect)
        elif self.moving_left:
            flip = self.run_animation[self.frame].copy()
            flip = pygame.transform.flip(flip, True, False)
            display.blit(flip, self.rect)
        else:
            if self.facing_right:
                display.blit(self.idle_animation[self.frame], self.rect)
            else:
                flip = self.idle_animation[self.frame].copy()
                flip = pygame.transform.flip(flip, True, False)
                display.blit(flip, self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y
    
    def get_rect(self):
        return self.rect

