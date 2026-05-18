# -*- coding: utf-8 -*-
"""
Script khởi chạy game với các tùy chọn
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("SPACE SHOOTER - AI VERSION")
print("=" * 60)
print("\nCác tùy chọn:")
print("1. Chơi mà không có AI (chế độ bình thường)")
print("2. Chơi với AI (BFS/DFS/A-star)")
print()

choice = input("Chọn tùy chọn (1-2): ").strip()

use_ai = False
if choice == "2":
    use_ai = True
    print("\nAI được kích hoạt!")
elif choice == "1":
    print("\nChế độ bình thường (không có AI)")
else:
    print("Lựa chọn không hợp lệ, sử dụng chế độ bình thường")

print("\nĐang khởi chạy game...")
print("Nhấn SPACE để bắn, mũi tên để di chuyển, ESC để thoát")
print()

try:
    # Monkey-patch trước khi import main
    import stage1
    import boss_stage
    
    original_run_stage1 = stage1.run_stage1
    original_run_boss_stage = boss_stage.run_boss_stage
    
    def run_stage1_with_ai(screen, clock, background, font_path=None, use_ai_param=False):
        return original_run_stage1(screen, clock, background, font_path, use_ai=use_ai)
    
    def run_boss_stage_with_ai(screen, clock, background, font_path=None, use_ai_param=False):
        return original_run_boss_stage(screen, clock, background, font_path, use_ai=use_ai)
    
    stage1.run_stage1 = run_stage1_with_ai
    boss_stage.run_boss_stage = run_boss_stage_with_ai
    
    # Giờ import main (sau khi đã monkey-patch)
    from main import main
    main()
    
except Exception as e:
    print(f"\n❌ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
