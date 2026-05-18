# -*- coding: utf-8 -*-
import pygame
import random
from utils import SCREEN_WIDTH, SCREEN_HEIGHT, load_image, YELLOW, CYAN, ORANGE, PURPLE, LIME

class PowerUp(pygame.sprite.Sprite):
    TYPES = {
        'health': {'color': (0, 255, 0), 'effect': 'Hồi phục', 'duration': 0},
        'shield': {'color': CYAN, 'effect': 'Khiên', 'duration': 8000},
        'fire_rate': {'color': ORANGE, 'effect': 'Tốc bắn', 'duration': 6000},
        'multi_shot': {'color': PURPLE, 'effect': 'Bắn đôi', 'duration': 10000},
        'ally': {'color': LIME, 'effect': 'Đồng minh', 'duration': 15000},
    }

    def __init__(self, x, y, powerup_type=None):
        super().__init__()
        if powerup_type is None:
            powerup_type = random.choice(list(self.TYPES.keys()))
        
        self.type = powerup_type
        self.info = self.TYPES[powerup_type]
        
        # Tạo hình ảnh powerup
        self.image = load_image(f'{powerup_type}.png')
        if not self.image or self.image.get_size() == (50, 50):  # Nếu là fallback đỏ
            self.image = pygame.Surface((30, 30))
            self.image.fill(self.info['color'])
            pygame.draw.circle(self.image, (255, 255, 255), (15, 15), 13, 2)
        else:
            # Scale ảnh xuống kích thước nhỏ hơn để hitbox phù hợp
            self.image = pygame.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT + 50:
            self.kill()


class Ally(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y):
        super().__init__()
        # Load ảnh ally và scale xuống kích thước nhỏ
        self.image = load_image('ally.png')
        if not self.image or self.image.get_size() == (50, 50):  # Nếu fallback
            self.image = pygame.Surface((25, 25))
            self.image.fill((100, 200, 255))
            pygame.draw.circle(self.image, (255, 255, 255), (12, 12), 10, 2)
        else:
            self.image = pygame.transform.scale(self.image, (25, 25))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = player_x - 50
        self.rect.centery = player_y
        self.target_x = player_x - 50
        self.target_y = player_y
        self.speed = 5
        self.shoot_delay = 400
        self.last_shot = pygame.time.get_ticks()

    def update(self, player_rect):
        # Theo dõi player
        self.target_x = player_rect.centerx - 50
        self.target_y = player_rect.centery
        
        # Di chuyển về vị trí mục tiêu
        if abs(self.rect.centerx - self.target_x) > self.speed:
            self.rect.centerx += self.speed if self.rect.centerx < self.target_x else -self.speed
        if abs(self.rect.centery - self.target_y) > self.speed:
            self.rect.centery += self.speed if self.rect.centery < self.target_y else -self.speed

    def shoot(self, all_sprites, bullets):
        from bullet import Bullet
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top, speed=-10)
            all_sprites.add(bullet)
            bullets.add(bullet)
