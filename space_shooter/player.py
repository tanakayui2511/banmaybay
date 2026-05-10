import pygame
from utils import SCREEN_WIDTH, SCREEN_HEIGHT, load_image, get_sound_manager
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('player.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 5
        self.hp = 100
        self.max_hp = 100
        
        self.shoot_delay = 250 # Thời gian trễ giữa các lần bắn (milliseconds)
        self.last_shot = pygame.time.get_ticks()
        
        # Power-up effects
        self.shield = False
        self.shield_end_time = 0
        self.fire_rate_multiplier = 1.0
        self.fire_rate_end_time = 0
        self.multi_shot = False
        self.multi_shot_end_time = 0
        self.allies = []

    def update(self):
        # Kiểm tra hết hạn power-ups
        now = pygame.time.get_ticks()
        
        if self.shield and now > self.shield_end_time:
            self.shield = False
        
        if self.fire_rate_multiplier > 1.0 and now > self.fire_rate_end_time:
            self.fire_rate_multiplier = 1.0
        
        if self.multi_shot and now > self.multi_shot_end_time:
            self.multi_shot = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            
        # Giữ player không bay ra ngoài màn hình
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        
        # Cập nhật đồng minh
        for ally in self.allies[:]:
            ally.update(self.rect)

    def shoot(self, all_sprites, bullets):
        now = pygame.time.get_ticks()
        delay = int(self.shoot_delay / self.fire_rate_multiplier)
        
        # Hạn chế số lượng đạn tối đa để tránh lag
        if len(bullets) > 50:
            return
        
        if now - self.last_shot > delay:
            self.last_shot = now
            # Phát âm thanh bắn
            sound_manager = get_sound_manager()
            sound_manager.play_sound('shoot_player')
            
            if self.multi_shot:
                # Bắn 2 viên
                bullet1 = Bullet(self.rect.centerx - 15, self.rect.top)
                bullet2 = Bullet(self.rect.centerx + 15, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
            else:
                # Bắn 1 viên
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
        
        # Đồng minh bắn
        for ally in self.allies:
            ally.shoot(all_sprites, bullets)
    
    def take_damage(self, damage):
        if self.shield:
            return False
        self.hp -= damage
        return self.hp <= 0
    
    def add_ally(self):
        from powerup import Ally
        ally = Ally(self.rect.centerx, self.rect.centery)
        self.allies.append(ally)
        return ally
    
    def apply_powerup(self, powerup_type, duration=0):
        if powerup_type == 'health':
            self.hp = min(self.hp + 30, self.max_hp)
        elif powerup_type == 'shield':
            self.shield = True
            self.shield_end_time = pygame.time.get_ticks() + duration
        elif powerup_type == 'fire_rate':
            self.fire_rate_multiplier = 1.5
            self.fire_rate_end_time = pygame.time.get_ticks() + duration
        elif powerup_type == 'multi_shot':
            self.multi_shot = True
            self.multi_shot_end_time = pygame.time.get_ticks() + duration
        elif powerup_type == 'ally':
            self.add_ally()
