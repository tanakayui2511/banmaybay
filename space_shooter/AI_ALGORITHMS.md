# Space Shooter - AI Algorithms Documentation

## Các Thuật Toán Đã Thêm

### 1. **BFS (Breadth-First Search)**
- **Mục đích**: Tìm đường đi ngắn nhất từ kẻ địch đến người chơi
- **Cách hoạt động**: Khám phá các ô lân cận ở cùng độ sâu trước khi đi sâu hơn
- **Ưu điểm**: Tìm đường đi ngắn nhất, dễ hiểu
- **Nhược điểm**: Sử dụng nhiều bộ nhớ
- **Sử dụng**: `algorithms.py` - hàm `PathFinding.bfs()`

### 2. **DFS (Depth-First Search)**
- **Mục đích**: Tìm đường đi bằng cách đi sâu vào không gian tìm kiếm
- **Cách hoạt động**: Khám phá một nhánh đến cuối cùng rồi quay lại
- **Ưu điểm**: Sử dụng ít bộ nhớ hơn BFS
- **Nhược điểm**: Không đảm bảo tìm được đường đi ngắn nhất
- **Sử dụng**: `algorithms.py` - hàm `PathFinding.dfs()`

### 3. **A-star (A*)**
- **Mục đích**: Tìm đường đi tối ưu dựa trên heuristic khoảng cách
- **Cách hoạt động**: Sử dụng công thức `f = g + h` 
  - `g`: Chi phí từ điểm bắt đầu
  - `h`: Heuristic (ước lượng đến đích)
- **Ưu điểm**: Nhanh nhất, tìm đường tối ưu
- **Nhược điểm**: Phức tạp hơn BFS/DFS
- **Sử dụng**: `algorithms.py` - hàm `PathFinding.astar()`

### 4. **Logistic Regression (Sigmoid Function)**
- **Mục đích**: Tính mức độ tấn công và trốn tránh của kẻ địch
- **Cách hoạt động**: Chuyển đổi các yếu tố (khoảng cách, HP, sát thương) thành xác suất (0-1)
- **Công thức**: `σ(x) = 1 / (1 + e^(-k(x-midpoint)))`
- **Ứng dụng**:
  - `LogisticBehavior.calculate_aggression()`: Tính mức độ tấn công
  - `LogisticBehavior.calculate_evasion()`: Tính mức độ trốn tránh
- **Sử dụng**: `algorithms.py` - class `LogisticBehavior`

## Cấu Trúc File

```
space_shooter/
├── algorithms.py      # Chứa các thuật toán (BFS, DFS, A-star, Logistic)
├── ai.py              # AI Controller cho kẻ địch và Boss
├── enemy.py           # Class Enemy với hỗ trợ AI
├── boss_stage.py      # Boss stage với AI cho Boss
├── stage1.py          # Stage 1 với AI cho enemies
├── main.py            # File chính
├── player.py          # Class Player
├── bullet.py          # Class Bullet
├── powerup.py         # Class PowerUp
└── utils.py           # Các hàm tiện ích
```

## Cách Sử Dụng

### Khởi tạo Enemy với AI
```python
# Sử dụng A-star (mặc định)
enemy = Enemy(algorithm='astar')

# Hoặc sử dụng BFS
enemy = Enemy(algorithm='bfs')

# Hoặc sử dụng DFS
enemy = Enemy(algorithm='dfs')
```

### Cập nhật Enemy
```python
# Truyền player_rect để AI tính toán
enemy.update(player_rect)
```

### Boss AI
```python
from ai import BossAI

boss_ai = BossAI(algorithm='astar')
action = boss_ai.update(boss_pos, player_pos, boss_hp, max_hp)
```

## Tùy chỉnh Hành vi AI

### Thay đổi Aggression Level
Sửa trong `algorithms.py`:
```python
aggression = LogisticBehavior.sigmoid(combined, midpoint=0.4, steepness=6)
# midpoint: điểm giữa (0-1)
# steepness: độ dốc (càng cao = đổi nhanh hơn)
```

### Thay đổi Tốc độ Tính Lại Đường Đi
Sửa trong `ai.py`:
```python
self.recalculate_interval = 30  # Mỗi 30 frame
```

## Hiệu Năng

| Thuật Toán | Tốc độ | Chính xác | Bộ nhớ |
|-----------|-------|----------|--------|
| BFS       | Trung bình | Cao | Cao |
| DFS       | Nhanh | Trung bình | Thấp |
| A-star    | Rất nhanh | Rất cao | Trung bình |

## Lưu Ý

1. A-star là thuật toán được khuyên dùng vì cân bằng tốt giữa hiệu suất và chính xác
2. Có thể tắt AI bằng cách set `enemy.use_ai = False`
3. Boss sẽ thay đổi hành vi theo HP (Phase 1, 2, 3)
4. Logistic regression giúp AI có hành vi tự nhiên hơn

## Tham khảo Thêm

- [Pathfinding: A* Algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [BFS and DFS](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Sigmoid Function](https://en.wikipedia.org/wiki/Sigmoid_function)
