import pygame
from utils import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, GREEN, RED, CYAN, load_image, get_sound_manager
from player import Player
from enemy import Enemy
from powerup import PowerUp, Ally


def draw_text(surface, text, size, x, y, color, font_path=None, center=False):
    if font_path:
        font = pygame.font.Font(font_path, size)
        font.set_bold(True)
    else:
        font = pygame.font.SysFont(None, size, bold=True)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)


def draw_hp_bar(surface, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 150
    BAR_HEIGHT = 15
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)


def run_stage1(screen, clock, background, font_path=None):
    running = True
    game_over = False
    game_over_sound_played = False
    score = 0

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    allies = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    for i in range(8):
        m = Enemy()
        all_sprites.add(m)
        enemies.add(m)

    bg_y1 = 0
    bg_y2 = -SCREEN_HEIGHT

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                player.shoot(all_sprites, player_bullets)

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
                player.shoot(all_sprites, player_bullets)

            all_sprites.update()
            
            # Cập nhật allies riêng
            for ally in player.allies:
                ally.update(player.rect)

            # Xóa enemy bullets ngoài màn hình để giảm lag
            for bullet in list(enemy_bullets):
                if bullet.rect.top > SCREEN_HEIGHT + 50:
                    enemy_bullets.remove(bullet)

            now = pygame.time.get_ticks()
            for enemy in enemies:
                if now - enemy.last_shot > enemy.shoot_delay:
                    enemy.last_shot = now
                    # Hạn chế số lượng enemy bullets
                    if len(enemy_bullets) < 30:
                        enemy.shoot(all_sprites, enemy_bullets)

            hits = pygame.sprite.groupcollide(enemies, player_bullets, True, True)
            for hit in hits:
                score += 10
                # Phát âm thanh nổ
                sound_manager = get_sound_manager()
                sound_manager.play_sound('explosion_small')
                # Ngẫu nhiên spawn power-up (giảm frequency để tối ưu)
                if pygame.time.get_ticks() % 4 < 2:
                    powerup = PowerUp(hit.rect.centerx, hit.rect.centery)
                    all_sprites.add(powerup)
                    powerups.add(powerup)
                m = Enemy()
                all_sprites.add(m)
                enemies.add(m)

            hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
            for hit in hits:
                sound_manager = get_sound_manager()
                sound_manager.play_sound('explosion_player')
                if player.take_damage(20):
                    game_over = True
                    game_over_sound_played = False

            hits = pygame.sprite.spritecollide(player, enemies, True)
            for hit in hits:
                sound_manager = get_sound_manager()
                sound_manager.play_sound('explosion_player')
                if player.take_damage(20):
                    game_over = True
                    game_over_sound_played = False
                m = Enemy()
                all_sprites.add(m)
                enemies.add(m)
            
            # Xử lý power-up
            powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
            for powerup in powerup_hits:
                player.apply_powerup(powerup.type, powerup.info['duration'])
                if powerup.type == 'ally':
                    ally = player.add_ally()
                    allies.add(ally)
                score += 50

        bg_y1 += 1
        bg_y2 += 1
        if bg_y1 >= SCREEN_HEIGHT:
            bg_y1 = -SCREEN_HEIGHT
        if bg_y2 >= SCREEN_HEIGHT:
            bg_y2 = -SCREEN_HEIGHT

        screen.blit(background, (0, bg_y1))
        screen.blit(background, (0, bg_y2))

        all_sprites.draw(screen)
        allies.draw(screen)
        draw_text(screen, f"Score: {score}", 20, 10, 10, WHITE, font_path)
        draw_hp_bar(screen, 10, 40, player.hp)
        
        # Vẽ shield indicator
        if player.shield:
            pygame.draw.circle(screen, CYAN, player.rect.center, 50, 3)
            draw_text(screen, "KHIEN", 16, player.rect.centerx, player.rect.centery + 60, CYAN, font_path, center=True)
        
        # Vẽ fire rate indicator
        if player.fire_rate_multiplier > 1.0:
            draw_text(screen, "TOC BAN", 14, SCREEN_WIDTH - 100, 10, RED, font_path)
        
        # Vẽ multi-shot indicator
        if player.multi_shot:
            draw_text(screen, "BAN DOI", 14, SCREEN_WIDTH - 100, 35, RED, font_path)
        
        # Vẽ allies count
        if player.allies:
            draw_text(screen, f"Dong minh: {len(player.allies)}", 14, SCREEN_WIDTH - 150, 60, GREEN, font_path)

        if game_over:
            if not game_over_sound_played:
                sound_manager = get_sound_manager()
                sound_manager.play_sound('game_over')
                game_over_sound_played = True
            draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, RED, font_path, center=True)
            draw_text(screen, "NHẤN R ĐỂ CHƠI LẠI", 28, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, WHITE, font_path, center=True)
            draw_text(screen, "NHẤN ESC để về menu", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70, WHITE, font_path, center=True)

        pygame.display.flip()

    return "menu"
