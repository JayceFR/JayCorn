import pygame
import math
class Bird():
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.speed = 3
        self.direction = 1
        self.max_x = self.x + 150
        self.min_x = self.x - 150
        self.display_x = 0
        self.display_y = 0
        self.offset = [0,0]
    
    def draw(self, display, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        pygame.draw.rect(display, (255,0,0), self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y
    
    def move(self, safe, player_x, player_y):
        point = (player_x , self.rect.y)
        l1 = math.sqrt(math.pow((point[0] - self.rect.x - self.offset[0]//2), 2) + math.pow((point[1] - self.rect.y + self.offset[1]//2), 2))
        l2 = math.sqrt(math.pow((player_x - point[0] - self.offset[0]//2), 2) + math.pow((player_y - point[1] + self.offset[1]//2), 2))
        angle = math.degrees(math.atan2(l2, l1))
        if self.rect.y  > player_y:
            if self.rect.x  > player_x:
                self.facing_right = False
                angle = 180 - angle
        else:
            if self.rect.x > player_x:
                angle = 180 + angle
            else:
                angle = 360 - angle
        if player_x >= self.min_x and player_x <= self.max_x and player_y >= self.rect.y:
            if not safe:
                self.rect.y -= math.sin(math.radians(angle)) * self.speed
                self.rect.x += math.cos(math.radians(angle)) * self.speed
            else:
                if self.rect.y > self.y:
                    self.rect.y -= 5
                self.rect.x += self.direction * self.speed
                if self.rect.x >= self.max_x:
                    self.direction *= -1
                elif self.rect.x <= self.min_x:
                    self.direction *= -1
        else:
            if self.rect.y > self.y:
                self.rect.y -= 5
            self.rect.x += self.direction * self.speed
            if self.rect.x >= self.max_x:
                self.direction *= -1
            elif self.rect.x <= self.min_x:
                self.direction *= -1
    
    def get_range(self):
        return [self.min_x, self.max_x]
