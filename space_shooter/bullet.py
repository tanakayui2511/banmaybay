import pygame
import math
from utils import load_image

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=-10, vx=0, vy=None):
        super().__init__()
        self.image = load_image('bullet.png')
        # Thu nhỏ hình ảnh đạn cho phù hợp
        self.image = pygame.transform.scale(self.image, (15, 35))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = abs(speed)
        if vy is None:
            self.vx = vx
            self.vy = speed
        else:
            self.vx = vx
            self.vy = vy

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        # Tự động hủy nếu đạn bay ra khỏi màn hình
        surface = pygame.display.get_surface()
        if surface is not None:
            height = surface.get_height()
            width = surface.get_width()
            if self.rect.bottom < 0 or self.rect.top > height or self.rect.right < 0 or self.rect.left > width:
                self.kill()
