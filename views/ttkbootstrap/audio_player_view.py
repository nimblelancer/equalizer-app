import ttkbootstrap as ttk
import random
from ttkbootstrap.constants import *
from tkinter import filedialog, PhotoImage
from viewmodels.audio_player_viewmodel import AudioPlayerViewModel
from PIL import Image, ImageTk

class AudioPlayerView(ttk.LabelFrame):
    def __init__(self, root, view_model: AudioPlayerViewModel):
        super().__init__(root, text="Audio Player")
        self.root = root
        self.view_model = view_model

        
        self.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        self.columnconfigure((0,1), weight=1)  # Giúp LabelFrame mở rộng theo chiều ngang
        self.rowconfigure((3), weight=1)  # Đảm bảo hàng cuối cùng không chiếm không gian thừa

        # Canvas random spectrogram
        self.canvas = ttk.Canvas(self, width=550, height=150, bg="#121212", highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.bars = []
        self.draw_random_spectrogram()
        self.update_random_spectrogram()

        # Thêm thanh trượt tiến trình bài hát
        self.progress_var = ttk.DoubleVar()
        self.progress_slider = ttk.Scale(
            self, from_=0, to=100, orient="horizontal", variable=self.progress_var, style="primary.TScale", command=self.seek_audio
        )
        self.progress_slider.grid(row=1, column=0, columnspan=3, padx=60, pady=5, sticky="ew")  # Đặt thanh giữa phổ và nút

        # Thời gian bắt đầu
        self.start_time_label = ttk.Label(self, text="0:00", bootstyle="light")
        self.start_time_label.grid(row=1, column=0, padx=10, sticky="w")

        # Thời gian còn lại
        self.remaining_time_label = ttk.Label(self, text="0:00", bootstyle="light")
        self.remaining_time_label.grid(row=1, column=2, padx=10, sticky="e")

        # Cập nhật tiến trình nhạc
        self.update_progress()

        # Thanh trượt âm lượng
        self.volume_icon = self.load_image_icon("assets/volume.png", (22, 22))

        # Tạo Frame chứa icon và slider
        self.vol_frame = ttk.Frame(self)
        self.vol_frame.grid(row=2, column=0, padx=20, sticky="ew")

        self.vol_label = ttk.Label(self.vol_frame, image=self.volume_icon)
        self.vol_label.grid(row=0, column=0, padx=10)

        # Thanh trượt âm lượng
        self.vol_slider = ttk.Scale(self.vol_frame, from_=0, to=5, orient="horizontal", style="primary.TScale", command=self.setting_volume)
        self.vol_slider.grid(row=0, column=1, padx=10)
        self.vol_slider.set(1)

        # Frame chứa nút điều khiển (Đặt ở giữa)
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")


        self.play_icon = self.load_image_icon("assets/play.png", (32, 32))
        self.pause_icon = self.load_image_icon("assets/pause.png", (32, 32))
        self.stop_icon = self.load_image_icon("assets/stop.png", (32, 32))
        self.resume_icon = self.load_image_icon("assets/resume.png", (32, 32))
        self.open_icon = self.load_image_icon("assets/open.png", (32, 32))

        self.play_button = ttk.Button(self.button_frame, image=self.play_icon, command=view_model.play_command, bootstyle="dark-link")    
        self.play_button.grid(row=0, column=0, padx=5)

        self.pause_button = ttk.Button(self.button_frame, image=self.pause_icon, command=view_model.pause_command, bootstyle="dark-link")
        self.pause_button.grid(row=0, column=1, padx=5)

        self.stop_button = ttk.Button(self.button_frame, image=self.stop_icon, command=view_model.stop_command, bootstyle="dark-link")
        self.stop_button.grid(row=0, column=2, padx=5)     

        self.unpause_button = ttk.Button(self.button_frame, image=self.resume_icon, command=view_model.unpause_command, bootstyle="dark-link")
        self.unpause_button.grid(row=0, column=3, padx=5)

        # Nút chọn file (Đặt sau cùng)
        self.select_file_button = ttk.Button(self, text="Open", command=self.select_file, bootstyle="outline-primary")
        self.select_file_button.grid(row=2, column=2, padx=20, sticky="w")


        self.view_model.add_view_listener(self)

    def on_close(self):
        self.quit()  # Dừng Tkinter loop
        self.destroy()  # Giải phóng bộ nhớ
        self.view_model.on_close()

    def draw_random_spectrogram(self):
        self.canvas.delete("all")
        for i in range(15):
            x = 20 + i * 35
            height = random.randint(20, 100)
            bar = self.canvas.create_rectangle(x, 150 - height, x + 15, 150, fill="#4581ec", outline="")
            self.bars.append(bar)

    def update_random_spectrogram(self):
        for i, bar in enumerate(self.bars):
            new_height = random.randint(20, 120)
            self.canvas.coords(bar, 20 + i * 35, 150 - new_height, 35 + i * 35, 150)
        self.root.after(500, self.update_random_spectrogram)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if file_path:
            self.view_model.select_file(file_path)

    def setting_volume(self, event=None):
        self.view_model.setting_volume(round(float(self.vol_slider.get()), 1))

    def load_image_icon(self, path, size):
        img = Image.open(path)
        img = img.resize(size, Image.LANCZOS)  # Resize bằng LANCZOS để giữ chất lượng
        return ImageTk.PhotoImage(img)

    # Seek
    def update_progress(self):
        pass

    def seek_audio(self, value):
        pass