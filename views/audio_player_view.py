from pathlib import Path
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from models import AudioPlayerModel

class AudioPlayerView(ttk.Labelframe):
    def __init__(self, master, view_model):
        super().__init__(master, text="Audio Player", padding=5)
        self.view_model = view_model
        self.view_model.set_view(self)
        self.pack(fill=BOTH, expand=YES)
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
            command=self.view_model.on_progress, 
            from_=0,
            to=100,
            value=0
        )
        self.scale.pack(side=LEFT, fill=X, expand=YES)
        self.scale.bind("<ButtonRelease-1>", self.view_model.on_progress_release)
        self.remain_label = ttk.Label(container, text='00:00')
        self.remain_label.pack(side=LEFT, padx=5)
    
    def create_buttonbox(self):
        """Tạo các nút điều khiển nhạc"""
        
        container = ttk.Frame(self)
        container.pack(fill=X, pady=5)

        # Các nút control cơ bản
        ttk.Button(container, text='Open', command=self.view_model.select_file).pack(side=LEFT, fill=X, expand=YES)
        ttk.Button(container, text='Play', command=self.view_model.play_audio).pack(side=LEFT, fill=X, expand=YES)
        ttk.Button(container, text='Pause', command=self.view_model.pause_audio).pack(side=LEFT, fill=X, expand=YES)
        ttk.Button(container, text='Stop', command=self.view_model.stop_audio).pack(side=LEFT, fill=X, expand=YES)

        # Voice Button
        ttk.Button(container, text='Voice', command=self.view_model.voice_action).pack(side=LEFT, fill=X, expand=YES)

        # Volume control
        volume_container = ttk.Frame(self)
        volume_container.pack(fill=X, pady=10)

        ttk.Label(volume_container, text="Volume").pack(side=LEFT, padx=5)

        self.volume_var = ttk.IntVar(value=50)
        self.volume_slider = ttk.Scale(
            master=volume_container,
            from_=1,
            to=100,
            orient=HORIZONTAL,
            variable=self.volume_var,
            command=self.view_model.setting_volume
        )
        self.volume_slider.pack(side=LEFT, fill=X, expand=YES, padx=5)