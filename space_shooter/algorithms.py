# -*- coding: utf-8 -*-
"""
Các thuật toán tìm kiếm và AI cho Space Shooter
"""

import math
from collections import deque
from utils import SCREEN_WIDTH, SCREEN_HEIGHT

class Node:
    """Node cho pathfinding"""
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0  # Chi phí từ điểm bắt đầu
        self.h = 0  # Heuristic (ước lượng đến đích)
        self.f = 0  # g + h

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class PathFinding:
    """Các thuật toán tìm đường"""
    
    GRID_SIZE = 50  # Kích thước mỗi ô trong lưới
    
    @staticmethod
    def get_grid_pos(x, y):
        """Chuyển đổi tọa độ pixel thành tọa độ lưới"""
        return (int(x // PathFinding.GRID_SIZE), int(y // PathFinding.GRID_SIZE))
    
    @staticmethod
    def get_pixel_pos(grid_x, grid_y):
        """Chuyển đổi tọa độ lưới thành tọa độ pixel"""
        return (grid_x * PathFinding.GRID_SIZE + PathFinding.GRID_SIZE // 2,
                grid_y * PathFinding.GRID_SIZE + PathFinding.GRID_SIZE // 2)
    
    @staticmethod
    def get_neighbors(node):
        """Lấy các nút lân cận (8 hướng)"""
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = node.x + dx, node.y + dy
                # Kiểm tra trong ranh giới màn hình
                if 0 <= nx * PathFinding.GRID_SIZE < SCREEN_WIDTH and \
                   0 <= ny * PathFinding.GRID_SIZE < SCREEN_HEIGHT:
                    neighbors.append(Node(nx, ny))
        return neighbors
    
    @staticmethod
    def heuristic(node, goal):
        """Heuristic Euclidean cho A-star"""
        return math.sqrt((node.x - goal.x)**2 + (node.y - goal.y)**2)
    
    @staticmethod
    def bfs(start_pos, goal_pos, max_steps=100):
        """
        BFS (Breadth-First Search) - Tìm đường ngắn nhất
        
        Args:
            start_pos: Tuple (x, y) vị trí bắt đầu
            goal_pos: Tuple (x, y) vị trí đích
            max_steps: Số bước tối đa
            
        Returns:
            List của các tọa độ pixel từ start đến goal
        """
        start = Node(*PathFinding.get_grid_pos(*start_pos))
        goal = Node(*PathFinding.get_grid_pos(*goal_pos))
        
        if start == goal:
            return [goal_pos]
        
        queue = deque([start])
        visited = {start}
        steps = 0
        
        while queue and steps < max_steps:
            current = queue.popleft()
            
            if current == goal:
                # Xây dựng đường đi
                path = []
                while current:
                    path.append(PathFinding.get_pixel_pos(current.x, current.y))
                    current = current.parent
                return path[::-1]
            
            for neighbor in PathFinding.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    neighbor.parent = current
                    queue.append(neighbor)
                    steps += 1
        
        return [start_pos]  # Không tìm thấy đường
    
    @staticmethod
    def dfs(start_pos, goal_pos, max_steps=100):
        """
        DFS (Depth-First Search) - Tìm đường bằng cách đi sâu
        
        Args:
            start_pos: Tuple (x, y) vị trí bắt đầu
            goal_pos: Tuple (x, y) vị trí đích
            max_steps: Số bước tối đa
            
        Returns:
            List của các tọa độ pixel từ start đến goal
        """
        start = Node(*PathFinding.get_grid_pos(*start_pos))
        goal = Node(*PathFinding.get_grid_pos(*goal_pos))
        
        if start == goal:
            return [goal_pos]
        
        stack = [start]
        visited = {start}
        steps = 0
        
        while stack and steps < max_steps:
            current = stack.pop()
            
            if current == goal:
                # Xây dựng đường đi
                path = []
                while current:
                    path.append(PathFinding.get_pixel_pos(current.x, current.y))
                    current = current.parent
                return path[::-1]
            
            for neighbor in PathFinding.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    neighbor.parent = current
                    stack.append(neighbor)
                    steps += 1
        
        return [start_pos]  # Không tìm thấy đường
    
    @staticmethod
    def astar(start_pos, goal_pos, max_steps=200):
        """
        A* (A-star) - Tìm đường tối ưu với heuristic
        
        Args:
            start_pos: Tuple (x, y) vị trí bắt đầu
            goal_pos: Tuple (x, y) vị trí đích
            max_steps: Số bước tối đa
            
        Returns:
            List của các tọa độ pixel từ start đến goal
        """
        start = Node(*PathFinding.get_grid_pos(*start_pos))
        goal = Node(*PathFinding.get_grid_pos(*goal_pos))
        
        if start == goal:
            return [goal_pos]
        
        start.h = PathFinding.heuristic(start, goal)
        start.f = start.h
        
        open_list = [start]
        closed_list = set()
        steps = 0
        
        while open_list and steps < max_steps:
            # Tìm node với f nhỏ nhất
            current_idx = 0
            for i, node in enumerate(open_list):
                if node.f < open_list[current_idx].f:
                    current_idx = i
            
            current = open_list.pop(current_idx)
            
            if current == goal:
                # Xây dựng đường đi
                path = []
                while current:
                    path.append(PathFinding.get_pixel_pos(current.x, current.y))
                    current = current.parent
                return path[::-1]
            
            closed_list.add(current)
            
            for neighbor in PathFinding.get_neighbors(current):
                if neighbor in closed_list:
                    continue
                
                neighbor.g = current.g + 1
                neighbor.h = PathFinding.heuristic(neighbor, goal)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current
                
                # Kiểm tra nếu đã trong open_list
                in_open = any(n == neighbor for n in open_list)
                if not in_open:
                    open_list.append(neighbor)
                
                steps += 1
        
        return [start_pos]  # Không tìm thấy đường


class LogisticBehavior:
    """Hàm logistic và hành vi AI"""
    
    @staticmethod
    def sigmoid(x, midpoint=0.5, steepness=5):
        """
        Hàm sigmoid/logistic
        Chuyển đổi giá trị liên tục thành xác suất từ 0-1
        
        Args:
            x: Giá trị đầu vào (0-1)
            midpoint: Điểm giữa (mặc định 0.5)
            steepness: Độ dốc (mặc định 5)
            
        Returns:
            Giá trị từ 0-1 (xác suất)
        """
        try:
            return 1 / (1 + math.exp(-steepness * (x - midpoint)))
        except:
            return 0.5
    
    @staticmethod
    def calculate_aggression(distance_to_player, current_hp, max_hp):
        """
        Tính mức độ tấn công dựa trên khoảng cách và sức khỏe
        
        Args:
            distance_to_player: Khoảng cách đến người chơi (0-1000+)
            current_hp: Sức khỏe hiện tại
            max_hp: Sức khỏe tối đa
            
        Returns:
            Giá trị 0-1 (mức độ tấn công)
        """
        # Chuẩn hóa khoảng cách (càng gần = càng cao)
        distance_factor = min(distance_to_player / 500, 1.0)
        closeness = 1 - distance_factor  # Đảo ngược
        
        # Chuẩn hóa HP (càng cao = càng tấn công mạnh)
        hp_factor = current_hp / max(max_hp, 1)
        
        # Kết hợp hai yếu tố
        combined = (closeness * 0.6 + hp_factor * 0.4)
        
        # Áp dụng sigmoid
        aggression = LogisticBehavior.sigmoid(combined, midpoint=0.4, steepness=6)
        
        return aggression
    
    @staticmethod
    def calculate_evasion(damage_taken_recent, max_hp):
        """
        Tính mức độ trốn tránh dựa trên sát thương gần đây
        
        Args:
            damage_taken_recent: Sát thương nhận trong vòng gần đây (0-max_hp)
            max_hp: Sức khỏe tối đa
            
        Returns:
            Giá trị 0-1 (mức độ trốn tránh)
        """
        damage_factor = min(damage_taken_recent / max(max_hp, 1), 1.0)
        evasion = LogisticBehavior.sigmoid(damage_factor, midpoint=0.3, steepness=5)
        return evasion


class AIBehavior:
    """Điều khiển hành vi AI"""
    
    @staticmethod
    def choose_action(distance_to_player, hp, max_hp, damage_taken, algorithm='astar'):
        """
        Chọn hành động dựa trên trạng thái và thuật toán
        
        Args:
            distance_to_player: Khoảng cách đến người chơi
            hp: Sức khỏe hiện tại
            max_hp: Sức khỏe tối đa
            damage_taken: Sát thương nhận gần đây
            algorithm: Thuật toán sử dụng ('bfs', 'dfs', 'astar')
            
        Returns:
            Dict với hành động {'type': ..., 'value': ...}
        """
        aggression = LogisticBehavior.calculate_aggression(distance_to_player, hp, max_hp)
        evasion = LogisticBehavior.calculate_evasion(damage_taken, max_hp)
        
        action = {
            'type': 'move',
            'direction': 0,
            'should_shoot': False,
            'aggression': aggression,
            'evasion': evasion
        }
        
        # Nếu mức tấn công cao và khoảng cách gần → tấn công
        if aggression > 0.6 and distance_to_player < 300:
            action['should_shoot'] = True
            action['direction'] = 1 if distance_to_player > 0 else -1
        
        # Nếu bị tổn thương nặng → trốn tránh
        if evasion > 0.7:
            action['direction'] = -1  # Chuyển động ngược
            action['type'] = 'evade'
        
        # Nếu hạ thấp → di chuyển quanh
        if hp < max_hp * 0.3:
            action['type'] = 'circle'
        
        return action
