from pathlib import Path

files = {}

files['bullet.py'] = {
    'old': """import pygame
import math
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
""",
    'new': """import pygame
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
"""
}

files['enemy.py'] = {
    'old': """    def shoot(self, all_sprites, enemy_bullets):
        bullet = Bullet(self.rect.centerx, self.rect.bottom, speed=6)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)
""",
    'new': """    def shoot(self, all_sprites, enemy_bullets, target_rect=None):
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
"""
}

files['boss_stage_shoot_enemy'] = {
    'old': """                    if len(enemy_bullets) < 30:
                        enemy.shoot(all_sprites, enemy_bullets)
""",
    'new': """                    if len(enemy_bullets) < 30:
                        enemy.shoot(all_sprites, enemy_bullets, player.rect)
"""
}

files['boss_stage_shoot_boss'] = {
    'old': """                if len(enemy_bullets) < 30:
                    boss.shoot(all_sprites, enemy_bullets)
""",
    'new': """                if len(enemy_bullets) < 30:
                    boss.shoot(all_sprites, enemy_bullets, player.rect)
"""
}

files['stage1_shoot'] = {
    'old': """                    if len(enemy_bullets) < 30:
                        enemy.shoot(all_sprites, enemy_bullets)
""",
    'new': """                    if len(enemy_bullets) < 30:
                        enemy.shoot(all_sprites, enemy_bullets, player.rect)
"""
}

for key, pair in files.items():

    if key in ['boss_stage_shoot_enemy','boss_stage_shoot_boss','stage1_shoot','enemy.py','bullet.py']:
        if key == 'enemy.py':
            path = Path('enemy.py')
        elif key == 'bullet.py':
            path = Path('bullet.py')
        elif key == 'boss_stage_shoot_enemy' or key == 'boss_stage_shoot_boss':
            path = Path('boss_stage.py')
        elif key == 'stage1_shoot':
            path = Path('stage1.py')
        else:
            continue
        content = path.read_text(encoding='utf-8')
        if pair['old'] not in content:
            raise SystemExit(f"Patch target not found in {path}: {key}")
        path.write_text(content.replace(pair['old'], pair['new']), encoding='utf-8')

print('Patch applied successfully')
