import pygame
import time
import threading

class AudioPlayerModel:
    def __init__(self):
        pygame.mixer.init()
        self.elapsed_var = 0
        self.remain_var = 0
        self.file_path = None
        self.is_paused = False
        self.duration = 0
        
    def load_file(self, file_path):
        self.file_path = file_path
        pygame.mixer.music.load(file_path)
        self.duration = pygame.mixer.Sound(file_path).get_length()  # Lấy duration thật
        self.elapsed_var = 0

    def play_music(self, callback):
        """Phát nhạc và cập nhật progress"""
        if self.file_path:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.play()
                threading.Thread(target=self.update_progress, args=(callback,), daemon=True).start()

    def pause_music(self):
        pygame.mixer.music.pause()
        self.is_paused = True

    def stop_music(self, callback):
        pygame.mixer.music.stop()
        self.is_paused = False
        self.elapsed_time = 0
        callback(0, self.duration)

    def update_progress(self, callback):
        """Cập nhật thời gian chạy bài hát"""
        while pygame.mixer.music.get_busy():
            if not self.is_paused:
                elapsed = pygame.mixer.music.get_pos() // 1000  # Lấy thời gian chạy (ms -> giây)
                callback(elapsed, self.duration)
            time.sleep(1)
    
    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f'{minutes:02}:{seconds:02}'
