import pygame
import random
import math
from utils import SCREEN_WIDTH, SCREEN_HEIGHT, load_image
from bullet import Bullet
from ai import EnemyAI

class Enemy(pygame.sprite.Sprite):
    def __init__(self, algorithm='astar'):
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
        
        # AI
        self.ai = EnemyAI(algorithm=algorithm)
        self.hp = 10
        self.max_hp = 10
        self.use_ai = False  # Mặc định không dùng AI (để an toàn)

    def update(self, player_rect=None):
        """
        Cập nhật trạng thái kẻ địch
        
        Args:
            player_rect: Rect của người chơi (nếu có dùng AI)
        """
        if self.use_ai and player_rect:
            try:
                # Sử dụng AI để tính toán hành động
                action = self.ai.update(
                    (self.rect.centerx, self.rect.centery),
                    (player_rect.centerx, player_rect.centery),
                    self.hp,
                    self.max_hp
                )

                if action['type'] == 'evade':
                    self.speedy = -abs(random.randrange(3, 6))
                elif action['type'] == 'circle':
                    angle = math.atan2(player_rect.centery - self.rect.centery,
                                       player_rect.centerx - self.rect.centerx)
                    self.rect.x += math.cos(angle + 0.5) * 3
                    self.speedy = random.randrange(1, 4)
                elif action.get('detected') and self.ai.path:
                    next_pos = self.ai.get_next_position(
                        (self.rect.centerx, self.rect.centery), speed=3)
                    self.rect.centerx = int(next_pos[0])
                    self.speedy = random.randrange(2, 5)
                else:
                    self.speedy = random.randrange(2, 6)
            except Exception:
                self.speedy = random.randrange(2, 6)
        else:
            # Chuyển động mặc định (không dùng AI)
            self.speedy = random.randrange(2, 6)
        
        # Di chuyển xuống
        self.rect.y += self.speedy
        
        # Nếu bay khỏi đáy màn hình thì reset lại lên trên để tái sử dụng
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 6)
            self.hp = self.max_hp

    def shoot(self, all_sprites, enemy_bullets, target_rect=None):
        if target_rect is not None:
            dx = target_rect.centerx - self.rect.centerx
            dy = target_rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)
            speed = 6
            if distance != 0:
                vx = dx / distance * speed
                vy = dy / distance * speed
            else:
                vx = 0
                vy = speed
            bullet = Bullet(self.rect.centerx, self.rect.bottom, speed=speed, vx=vx, vy=vy)
        else:
            bullet = Bullet(self.rect.centerx, self.rect.bottom, speed=6)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)