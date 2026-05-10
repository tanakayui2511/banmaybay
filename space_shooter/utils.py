import os
import pygame
import math

# Màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PURPLE = (200, 0, 255)
LIME = (50, 205, 50)

# Đường dẫn thư mục
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets', 'images')
# SOUNDS_DIR = os.path.join(BASE_DIR, 'assets', 'sounds')

# Khởi tạo thư mục sounds nếu chưa có
#if not os.path.exists(SOUNDS_DIR):
#    os.makedirs(SOUNDS_DIR)

def load_image(filename, use_colorkey=True):
    path = os.path.join(ASSETS_DIR, filename)
    try:
        image = pygame.image.load(path)
        if image.get_alpha() is not None:
            image = image.convert_alpha()
        else:
            image = image.convert()

        if use_colorkey:
            # Bỏ nền đen (do ảnh AI tạo thường có nền đen)
            image.set_colorkey(BLACK)
        return image
    except Exception as e:
        print(f"Error loading image {filename}: {e}")
        # Trả về một khối vuông đỏ nếu không load được ảnh
        surf = pygame.Surface((50, 50))
        surf.fill(RED)
        return surf


def make_sound(frequency, duration, volume=0.3):
    """Tạo âm thanh với tần số và độ dài xác định"""
    sample_rate = 22050
    frames = int(sample_rate * duration)
    
    # Tạo mảng dữ liệu âm thanh
    arr = []
    for i in range(frames):
        # Tính giá trị sine wave
        value = math.sin(2.0 * math.pi * frequency * i / sample_rate)
        # Giảm âm lượng ở cuối để tránh "pop" sound
        if i > frames - sample_rate // 20:
            fade_factor = 1.0 - (i - (frames - sample_rate // 20)) / (sample_rate // 20)
            value *= fade_factor
        # Áp dụng âm lượng
        value *= volume * 32767
        arr.append(int(value))
    
    # Chuyển đổi thành byte array
    sound_data = bytes(arr[i % len(arr)] & 0xFF for i in range(len(arr) * 2))
    
    # Tạo pygame Sound object
    sound = pygame.mixer.Sound(buffer=sound_data)
    return sound


def make_complex_sound(frequencies, durations, volume=0.3):
    """Tạo âm thanh phức tạp từ danh sách tần số"""
    sample_rate = 22050
    total_frames = sum(int(sample_rate * d) for d in durations)
    
    arr = []
    current_frame = 0
    
    for freq, dur in zip(frequencies, durations):
        frames = int(sample_rate * dur)
        for i in range(frames):
            # Tính giá trị sine wave
            value = math.sin(2.0 * math.pi * freq * i / sample_rate)
            # Fade in/out
            if i < 100:
                value *= i / 100.0
            elif i > frames - 100:
                value *= 1.0 - (i - (frames - 100)) / 100.0
            # Áp dụng âm lượng
            value *= volume * 32767
            arr.append(int(value))
        current_frame += frames
    
    # Chuyển đổi thành byte array
    sound_data = bytes(arr[i % len(arr)] & 0xFF for i in range(len(arr) * 2))
    sound = pygame.mixer.Sound(buffer=sound_data)
    return sound


class SoundManager:
    """Quản lý các âm thanh trong trò chơi"""
    def __init__(self):
        self.sounds = {}
        self.current_music = None
        self.music_volume = 0.3
        self.sfx_volume = 0.5
        
        # Tạo các âm thanh
        self._create_sounds()
    
    def _create_sounds(self):
        """Tạo tất cả các hiệu ứng âm thanh"""
        try:
            # Âm thanh bắn (dùng cho Player)
            self.sounds['shoot_player'] = make_complex_sound(
                frequencies=[800, 1200],
                durations=[0.05, 0.05],
                volume=self.sfx_volume
            )
            
            # Âm thanh khi máy bay bị bắn hạ
            self.sounds['explosion_small'] = make_complex_sound(
                frequencies=[400, 200, 100],
                durations=[0.1, 0.1, 0.1],
                volume=self.sfx_volume
            )
            
            # Âm thanh khi Player bị bắn hạ
            self.sounds['explosion_player'] = make_complex_sound(
                frequencies=[600, 300, 150, 75],
                durations=[0.15, 0.15, 0.15, 0.2],
                volume=self.sfx_volume
            )
            
            # Âm thanh thua game
            self.sounds['game_over'] = make_complex_sound(
                frequencies=[500, 400, 300, 200],
                durations=[0.2, 0.2, 0.2, 0.3],
                volume=self.sfx_volume
            )
            
            # Âm thanh thắng Boss
            self.sounds['boss_defeated'] = make_complex_sound(
                frequencies=[800, 1000, 1200, 1400, 1600],
                durations=[0.1, 0.1, 0.1, 0.1, 0.2],
                volume=self.sfx_volume
            )
            
        except Exception as e:
            print(f"Error creating sounds: {e}")
    
    def play_sound(self, sound_name, loops=0):
        """Phát âm thanh"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                return self.sounds[sound_name].play(loops)
            except Exception as e:
                print(f"Error playing sound {sound_name}: {e}")
    
    def play_music(self, sound_name, loops=-1):
        """Phát âm nhạc nền"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                if self.current_music:
                    self.current_music.stop()
                self.current_music = self.sounds[sound_name].play(loops)
            except Exception as e:
                print(f"Error playing music {sound_name}: {e}")
    
    def stop_music(self):
        """Dừng âm nhạc nền"""
        if self.current_music:
            self.current_music.stop()
            self.current_music = None
    
    def set_sfx_volume(self, volume):
        """Đặt âm lượng hiệu ứng âm thanh"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def set_music_volume(self, volume):
        """Đặt âm lượng âm nhạc"""
        self.music_volume = max(0.0, min(1.0, volume))


# Tạo instance global của SoundManager
sound_manager = None

def init_sound_manager():
    """Khởi tạo SoundManager"""
    global sound_manager
    if sound_manager is None:
        sound_manager = SoundManager()
    return sound_manager

def get_sound_manager():
    """Lấy instance SoundManager"""
    global sound_manager
    if sound_manager is None:
        sound_manager = SoundManager()
    return sound_manager
    

