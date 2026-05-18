# -*- coding: utf-8 -*-
"""
AI Controller cho các đối tượng trong game
"""

from algorithms import PathFinding, LogisticBehavior, AIBehavior
import pygame
import random
import math

class EnemyAI:
    """Điều khiển AI cho quân địch"""
    
    def __init__(self, algorithm='astar'):
        """
        Args:
            algorithm: 'bfs', 'dfs', hoặc 'astar'
        """
        self.algorithm = algorithm
        self.path = []
        self.path_index = 0
        self.recalculate_timer = 0
        self.recalculate_interval = 30  # Tính lại đường đi mỗi 30 frame
        self.damage_taken_recent = 0
        self.damage_decay = 0.98  # Giảm damage_taken theo thời gian
        self.detected = False
    
    def update(self, enemy_pos, player_pos, enemy_hp, max_hp, delta_time=1):
        """
        Cập nhật logic AI
        
        Args:
            enemy_pos: Tuple (x, y) vị trí kẻ địch
            player_pos: Tuple (x, y) vị trí người chơi
            enemy_hp: Sức khỏe kẻ địch
            max_hp: Sức khỏe tối đa
            delta_time: Thời gian delta
            
        Returns:
            Dict hành động
        """
        # Giảm damage_taken_recent
        self.damage_taken_recent *= self.damage_decay
        
        # Tính khoảng cách tới người chơi
        dx = player_pos[0] - enemy_pos[0]
        dy = player_pos[1] - enemy_pos[1]
        distance = math.hypot(dx, dy)
        
        # Nếu người chơi ở trong tầm gặp, AI sẽ nhận dạng và lập đường đi
        self.detected = distance < 1000
        if self.detected:
            self.recalculate_timer -= 1
            if self.recalculate_timer <= 0:
                self._calculate_path(enemy_pos, player_pos)
                self.recalculate_timer = self.recalculate_interval
            action = AIBehavior.choose_action(distance, enemy_hp, max_hp,
                                             self.damage_taken_recent,
                                             self.algorithm)
            action['detected'] = True
        else:
            action = {
                'type': 'patrol',
                'direction': random.choice([-1, 1]),
                'should_shoot': False,
                'aggression': 0.0,
                'evasion': 0.0,
                'detected': False
            }
        
        return action
    
    def _calculate_path(self, start, goal):
        """Tính đường đi bằng thuật toán được chọn"""
        try:
            if self.algorithm == 'bfs':
                self.path = PathFinding.bfs(start, goal)
            elif self.algorithm == 'dfs':
                self.path = PathFinding.dfs(start, goal)
            else:  # astar (mặc định)
                self.path = PathFinding.astar(start, goal)
            
            self.path_index = 0
        except:
            self.path = []
    
    def get_next_position(self, current_pos, speed=2):
        """Lấy vị trí tiếp theo trên đường đi"""
        if not self.path or self.path_index >= len(self.path):
            return current_pos
        
        target = self.path[self.path_index]
        
        # Nếu gần đủ gần đích trong path → tiếp tục
        dx = target[0] - current_pos[0]
        dy = target[1] - current_pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < speed:
            self.path_index += 1
            if self.path_index >= len(self.path):
                return current_pos
            target = self.path[self.path_index]
            dx = target[0] - current_pos[0]
            dy = target[1] - current_pos[1]
            distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            ratio = speed / distance
            new_x = current_pos[0] + dx * ratio
            new_y = current_pos[1] + dy * ratio
            return (new_x, new_y)
        
        return current_pos
    
    def record_damage(self, damage):
        """Ghi nhận sát thương"""
        self.damage_taken_recent += damage


class BossAI(EnemyAI):
    """AI đặc biệt cho Boss"""
    
    def __init__(self, algorithm='astar'):
        super().__init__(algorithm)
        self.recalculate_interval = 60  # Boss tính lại ít thường xuyên hơn
        self.phase = 1  # Phase 1, 2, 3 của boss
    
    def update(self, boss_pos, player_pos, boss_hp, max_hp, delta_time=1):
        """Cập nhật Boss AI với các phase"""
        # Xác định phase dựa trên HP
        if boss_hp > max_hp * 0.66:
            self.phase = 1
        elif boss_hp > max_hp * 0.33:
            self.phase = 2
        else:
            self.phase = 3
        
        action = super().update(boss_pos, player_pos, boss_hp, max_hp, delta_time)
        
        # Boss càng yếu càng tấn công nhiều hơn
        phase_multiplier = 1 + (self.phase - 1) * 0.5
        action['aggression'] *= phase_multiplier
        
        # Phase 3 → tấn công liên tục
        if self.phase == 3:
            action['should_shoot'] = True
        
        return action
