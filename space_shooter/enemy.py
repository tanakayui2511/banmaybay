import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT, load_image
from bullet import Bullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('enemy.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        
        # Sinh ngẫu nhiên ở mép trên màn hình
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        
        # Tốc độ ngẫu nhiên
        self.speedy = random.randrange(2, 6)
        self.shoot_delay = random.randrange(1500, 3500)
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speedy
        
        # Nếu bay khỏi đáy màn hình thì reset lại lên trên để tái sử dụng
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 6)

    def shoot(self, all_sprites, enemy_bullets):
        bullet = Bullet(self.rect.centerx, self.rect.bottom, speed=6)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)
