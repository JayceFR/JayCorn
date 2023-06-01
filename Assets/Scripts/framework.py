import pygame
class Player():
    def __init__(self, x, y, width, height) -> None:
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
    
    def move(self, tiles):
        self.movement = [0, 0]
        if self.moving_right:
            self.movement[0] += self.speed
            self.moving_right = False
        if self.moving_left:
            self.movement[0] -= self.speed
            self.moving_left = False

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
        pygame.draw.rect(display, (255,0,0), self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y
    
    def get_rect(self):
        return self.rect

