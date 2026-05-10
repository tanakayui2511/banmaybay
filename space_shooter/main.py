# -*- coding: utf-8 -*-
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pygame
from utils import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, GREEN, RED, load_image
from stage1 import run_stage1
from boss_stage import run_boss_stage

# Khởi tạo pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

FONT_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'fonts', 'NotoSans-Regular.ttf')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter - Bắn Máy Bay")
clock = pygame.time.Clock()

# Load hình nền
background = load_image('background.png', use_colorkey=False)
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_text(surface, text, size, x, y, color, center=False):
    if FONT_PATH:
        font = pygame.font.Font(FONT_PATH, size)
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


def main_menu():
    options = ["Màn 1", "Màn 2 - Boss", "Hướng dẫn", "Thoát game"]
    selected = 0

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(options)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if selected == 0:
                        return "stage1"
                    if selected == 1:
                        return "boss"
                    if selected == 2:
                        return "help"
                    return "exit"
                elif event.key == pygame.K_ESCAPE:
                    return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, option in enumerate(options):
                    text_y = 260 + i * 70
                    option_rect = pygame.Rect(SCREEN_WIDTH // 2 - 180, text_y - 30, 360, 60)
                    if option_rect.collidepoint(event.pos):
                        if i == 0:
                            return "stage1"
                        if i == 1:
                            return "boss"
                        if i == 2:
                            return "help"
                        return "exit"

        screen.blit(background, (0, 0))
        draw_text(screen, "SPACE SHOOTER", 64, SCREEN_WIDTH // 2, 120, WHITE, center=True)
        draw_text(screen, "Sử dụng UP/DOWN hoặc chuột, ENTER để chọn", 24, SCREEN_WIDTH // 2, 190, WHITE, center=True)

        for i, option in enumerate(options):
            text_y = 260 + i * 70
            if i == selected:
                pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 190, text_y - 30, 380, 60), 3)
                draw_text(screen, option, 48, SCREEN_WIDTH // 2, text_y, RED, center=True)
            else:
                draw_text(screen, option, 48, SCREEN_WIDTH // 2, text_y, WHITE, center=True)

        pygame.display.flip()


def show_instructions():
    lines = [
        "Hướng dẫn chơi Space Shooter:",
        "- Di chuyển: Mũi tên trái/phải hoặc A/D",
        "- Bắn: Nhấn SPACE liên tục",
        "- Tránh đụng kẻ địch",
        "- Mỗi lần trúng: mất 20 HP",
        "- GAME OVER khi HP <= 0",
        "Nhấn ESC hoặc Backspace để quay lại menu.",
    ]

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_RETURN):
                    return "menu"

        screen.blit(background, (0, 0))
        draw_text(screen, "HƯỚNG DẪN", 64, SCREEN_WIDTH // 2, 80, WHITE, center=True)

        for index, line in enumerate(lines):
            draw_text(screen, line, 28, SCREEN_WIDTH // 2, 180 + index * 40, WHITE, center=True)

        pygame.display.flip()


def main():
    while True:
        choice = main_menu()
        if choice == "exit":
            break
        if choice == "help":
            next_screen = show_instructions()
            if next_screen == "exit":
                break
            continue
        if choice == "stage1":
            next_screen = run_stage1(screen, clock, background, FONT_PATH)
            if next_screen == "exit":
                break
            if next_screen == "restart":
                continue
            if next_screen == "menu":
                continue
        if choice == "boss":
            next_screen = run_boss_stage(screen, clock, background, FONT_PATH)
            if next_screen == "exit":
                break
            if next_screen == "restart":
                continue
            if next_screen == "menu":
                continue

    pygame.quit()


if __name__ == '__main__':
    main()
