import pygame

class Acorn():
    def __init__(self, x, y, width, height, idle_animation) -> None:
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.idle_animation = idle_animation
        self.movement = [0,0]
        self.frame = 0
        self.frame_last_update = 0
        self.frame_cooldown = 200
        self.collision_type = {}
    
    def draw(self, display, scroll):
        display.blit(self.idle_animation[self.frame], (self.rect.x - scroll[0], self.rect.y - scroll[1]))
    
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
            if not tile.ramp:
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
            if not tile.ramp:
                if self.movement[1] > 0:
                    self.rect.bottom = tile.get_rect().top
                    collision_types["bottom"][0] = True
                    collision_types["bottom"][1].append(tile)
                if self.movement[1] < 0:
                    self.rect.top = tile.get_rect().bottom
                    collision_types["top"][0] = True
                    collision_types['top'][1].append(tile)
        return collision_types

    def move(self, time, tiles):
        if time - self.frame_last_update > self.frame_cooldown:
            self.frame += 1
            if self.frame >= 4:
                self.frame = 0
            self.frame_last_update = time
        self.movement = [0,0]

        self.movement[1] += 8

        self.collision_type = self.collision_checker(tiles)
    
    def get_rect(self):
        return self.rect

