import pygame

class Chuma():
    def __init__(self, animation) -> None:
        self.animation = animation
        self.frame = 0
        self.frame_upate = 0
        self.frame_cooldown = 200

    def draw(self, time, display, scroll, loc):
        display.blit(self.animation[self.frame], (loc[0] - scroll[0], loc[1] - scroll[1]))
        if time - self.frame_upate > self.frame_cooldown:
            self.frame_upate = time
            self.frame += 1
            if self.frame >= 4:
                self.frame = 0
    
    def reset_frame(self):
        self.frame = 0
    