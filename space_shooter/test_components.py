# -*- coding: utf-8 -*-
"""
Script kiểm tra lỗi cơ bản
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("KIỂM TRA CÁC COMPONENTS")
print("=" * 60)

# Test 1: Import modules
print("\n[1] Kiểm tra import...")
try:
    from algorithms import PathFinding, LogisticBehavior, AIBehavior
    print("  ✓ algorithms.py")
except Exception as e:
    print(f"  ✗ algorithms.py: {e}")
    sys.exit(1)

try:
    from ai import EnemyAI, BossAI
    print("  ✓ ai.py")
except Exception as e:
    print(f"  ✗ ai.py: {e}")
    sys.exit(1)

try:
    from enemy import Enemy
    print("  ✓ enemy.py")
except Exception as e:
    print(f"  ✗ enemy.py: {e}")
    sys.exit(1)

try:
    from boss_stage import Boss
    print("  ✓ boss_stage.py (Boss class)")
except Exception as e:
    print(f"  ✗ boss_stage.py: {e}")
    sys.exit(1)

# Test 2: Tạo objects
print("\n[2] Kiểm tra tạo objects...")
try:
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test")
    
    # Tạo Enemy
    enemy = Enemy()
    print(f"  ✓ Enemy tạo thành công")
    print(f"    - Position: ({enemy.rect.x}, {enemy.rect.y})")
    print(f"    - use_ai: {enemy.use_ai}")
    
    # Tạo Boss
    boss = Boss()
    print(f"  ✓ Boss tạo thành công")
    print(f"    - Position: ({boss.rect.x}, {boss.rect.y})")
    print(f"    - use_ai: {boss.use_ai}")
    print(f"    - HP: {boss.hp}/{boss.max_hp}")
    
except Exception as e:
    print(f"  ✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Update objects
print("\n[3] Kiểm tra update (không AI)...")
try:
    # Update Enemy
    for i in range(3):
        enemy.update()
    print(f"  ✓ Enemy.update() thành công")
    print(f"    - Position sau 3 frames: ({enemy.rect.x}, {enemy.rect.y})")
    
    # Update Boss
    boss.speedx = 4
    for i in range(3):
        boss.rect.x += boss.speedx
        if boss.rect.left < 0 or boss.rect.right > 800:
            boss.speedx *= -1
    print(f"  ✓ Boss di chuyển thành công")
    print(f"    - Position sau 3 frames: ({boss.rect.x}, {boss.rect.y})")
    print(f"    - Vẫn trong khung hình: {0 <= boss.rect.x <= 800 - boss.rect.width}")
    
except Exception as e:
    print(f"  ✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Kiểm tra boundary checking
print("\n[4] Kiểm tra boundary (ranh giới)...")
try:
    boss.rect.x = 0
    boss.speedx = 5
    boss.rect.x += boss.speedx
    if boss.rect.right > 800:
        boss.rect.right = 800
        boss.speedx = -abs(boss.speedx)
    
    print(f"  ✓ Boss boundary check hoạt động")
    print(f"    - Position: {boss.rect.x}, right: {boss.rect.right}")
    print(f"    - Speedx: {boss.speedx}")
    print(f"    - Vẫn trong khung hình: {0 <= boss.rect.x <= 800 - boss.rect.width}")
    
except Exception as e:
    print(f"  ✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

pygame.quit()

print("\n" + "=" * 60)
print("✓ TẤT CẢ KIỂM TRA THÀNH CÔNG!")
print("=" * 60)
print("\nGi chạy game bằng một trong các cách:")
print("  1. python main.py (không AI)")
print("  2. python run_game.py (chọn AI hoặc không AI)")
