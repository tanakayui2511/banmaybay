# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("Testing imports...")

try:
    from algorithms import PathFinding, LogisticBehavior, AIBehavior
    print("✓ algorithms.py imported successfully")
except Exception as e:
    print(f"✗ Failed to import algorithms: {e}")
    sys.exit(1)

try:
    from ai import EnemyAI, BossAI
    print("✓ ai.py imported successfully")
except Exception as e:
    print(f"✗ Failed to import ai: {e}")
    sys.exit(1)

try:
    from enemy import Enemy
    print("✓ enemy.py imported successfully")
except Exception as e:
    print(f"✗ Failed to import enemy: {e}")
    sys.exit(1)

print("\nTesting Enemy creation...")
try:
    enemy = Enemy()
    enemy.use_ai = False  # Tắt AI
    print(f"✓ Enemy created: {enemy}")
    print(f"  - Position: ({enemy.rect.x}, {enemy.rect.y})")
    print(f"  - HP: {enemy.hp}/{enemy.max_hp}")
except Exception as e:
    print(f"✗ Failed to create enemy: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nTesting Enemy update (without AI)...")
try:
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test")
    
    for i in range(5):
        enemy.update()
        print(f"  Frame {i+1}: y={enemy.rect.y}, speedy={enemy.speedy}")
    
    pygame.quit()
    print("✓ Enemy update successful")
except Exception as e:
    print(f"✗ Failed to update enemy: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ All tests passed!")
