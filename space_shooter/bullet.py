import pygame
from utils import load_image

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=-10):
        super().__init__()
        self.image = load_image('bullet.png')
        # Thu nhỏ hình ảnh đạn cho phù hợp
        self.image = pygame.transform.scale(self.image, (15, 35))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        # Tự động hủy nếu đạn bay ra khỏi màn hình
        if self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height():
            self.kill()
