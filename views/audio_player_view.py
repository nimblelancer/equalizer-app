from pathlib import Path
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from tkinter import filedialog
from models import AudioPlayerModel

class AudioPlayerView(ttk.Labelframe):
    def __init__(self, master):
        super().__init__(master, text="Audio Player", padding=5)
        self.pack(fill=BOTH, expand=YES)
        
        self.player = AudioPlayerModel()
        self.player.elapsed_var = ttk.DoubleVar(value=0)
        self.player.remain_var = ttk.DoubleVar(value=190)
        self.create_media_window()
        self.create_progress_meter()
        self.create_buttonbox()
    
    def create_media_window(self):
        """Hiển thị ảnh nền cho media player"""
        img_path = Path(__file__).parent.parent / 'assets/mp_background.png'
        img = Image.open(img_path)
        img = img.resize((200, 200))
        self.demo_media = ImageTk.PhotoImage(img)
        self.media = ttk.Label(self, image=self.demo_media)
        self.media.pack(anchor=CENTER)
    
    def create_progress_meter(self):
        """Tạo thanh hiển thị tiến trình phát nhạc"""
        container = ttk.Frame(self)
        container.pack(fill=X, pady=10)
        
        self.elapse_label = ttk.Label(container, text='00:00')
        self.elapse_label.pack(side=LEFT, padx=5)
        
        self.scale = ttk.Scale(
            master=container, 
            command=self.on_progress, 
            from_=0,
            to=100,
            value=0
        )
        self.scale.pack(side=LEFT, fill=X, expand=YES)
        
        self.remain_label = ttk.Label(container, text='00:00')
        self.remain_label.pack(side=LEFT, padx=5)
    
    def create_buttonbox(self):
        """Tạo các nút điều khiển nhạc"""
        container = ttk.Frame(self)
        container.pack(fill=X)
        
        ttk.Button(container, text='Open', command=self.open_file).pack(side=LEFT, fill=X, expand=YES)
        ttk.Button(container, text='Play', command=self.play_music).pack(side=LEFT, fill=X, expand=YES)
        ttk.Button(container, text='Pause', command=self.pause_music).pack(side=LEFT, fill=X, expand=YES)
        ttk.Button(container, text='Stop', command=self.stop_music).pack(side=LEFT, fill=X, expand=YES)
    
    def open_file(self):
        """Chọn file nhạc từ máy"""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.player.load_file(file_path)
            self.play_music()
    
    def play_music(self):
        """Phát nhạc và cập nhật thanh progress"""
        self.player.play_music(self.update_progress)
    
    def pause_music(self):
        """Tạm dừng nhạc"""
        self.player.pause_music()
    
    def stop_music(self):
        """Dừng nhạc và reset thanh progress"""
        self.player.stop_music(self.update_progress)
    
    def update_progress(self, elapsed, duration):
        """Cập nhật thanh progress khi bài hát chạy"""
        if duration > 0:
            progress = (elapsed / duration) * 100
            self.scale.set(progress)  # Cập nhật thanh trượt progress bar
            self.elapse_label.config(text=self.player.format_time(int(elapsed)))  # Chuyển elapsed về int
            self.remain_label.config(text=self.player.format_time(int(duration - elapsed))) 
    
    def on_progress(self, val):
        """Update progress labels when the scale is updated."""
        total = self.player.duration

        elapse = int(float(val) * total)
        remain_tot = total - elapse

        self.player.elapsed_var = elapse
        self.player.remain_var = remain_tot

        self.elapse_label.config(text=self.player.format_time(elapse))
        self.remain_label.config(text=self.player.format_time(remain_tot))
