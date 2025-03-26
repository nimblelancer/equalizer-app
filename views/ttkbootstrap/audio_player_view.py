import ttkbootstrap as ttk
import random
from ttkbootstrap.constants import *
from tkinter import filedialog, PhotoImage
from viewmodels.audio_player_viewmodel import AudioPlayerViewModel
from PIL import Image, ImageTk
from models.audio_player_model import AudioPlayerState

class AudioPlayerView(ttk.LabelFrame):
    def __init__(self, root, view_model: AudioPlayerViewModel):
        super().__init__(root, text="Audio Player")
        self.root = root
        self.view_model = view_model
        self.view_model.set_update_callback(self.update_buttons)
        
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
        self.mute_icon = self.load_image_icon("assets/mute.png", (22, 22))

        # Tạo Frame chứa icon và slider
        self.vol_frame = ttk.Frame(self)
        self.vol_frame.grid(row=2, column=0, padx=20, sticky="ew")

        # Nút icon volume (thay vì Label, chuyển thành Button để click được)
        self.vol_button = ttk.Button(self.vol_frame, image=self.volume_icon, command=self.toggle_mute)
        self.vol_button.grid(row=0, column=0, padx=10)

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
        self.voice = self.load_image_icon("assets/voice.png", (32, 32))
        self.stop_voice = self.load_image_icon("assets/stopvoice.png", (32, 32))

        self.play_button = ttk.Button(self.button_frame, image=self.play_icon, bootstyle="dark-link", command=view_model.play_command, )    
        self.play_button.grid(row=0, column=0, padx=5)

        self.pause_button = ttk.Button(self.button_frame, image=self.pause_icon, bootstyle="dark-link", command=view_model.pause_command)
        self.pause_button.grid(row=0, column=1, padx=5)

        self.resume_button = ttk.Button(self.button_frame, image=self.resume_icon, bootstyle="dark-link", command=view_model.unpause_command)
        self.resume_button.grid(row=0, column=1, padx=5)

        self.stop_button = ttk.Button(self.button_frame, image=self.stop_icon, bootstyle="dark-link", command=view_model.stop_command)
        self.stop_button.grid(row=0, column=2, padx=5)     

        self.voice_button = ttk.Button(self.button_frame, image=self.voice, bootstyle="dark-link", command=view_model.voice_command)
        self.voice_button.grid(row=0, column=3, padx=5)

        self.stop_voice_button = ttk.Button(self.button_frame, image=self.stop_voice, bootstyle="dark-link", command=view_model.stop_command)
        self.stop_voice_button.grid(row=0, column=3, padx=5)

        # Nút chọn file (Đặt sau cùng)
        self.select_file_button = ttk.Button(self, text="Open", command=self.select_file, bootstyle="outline-primary")
        self.select_file_button.grid(row=2, column=2, padx=20, sticky="w")

        self.view_model.add_view_listener(self)
        self.update_buttons()

    def on_close(self):
        self.quit()  # Dừng Tkinter loop
        self.destroy()  # Giải phóng bộ nhớ
        self.view_model.on_close()

    def draw_random_spectrogram(self):
        self.canvas.delete("all")
        self.bars = []

        for i in range(15):
            x = 20 + i * 35
            height = random.randint(20, 100)
            
            # Giảm chiều cao thanh bar để tránh oval bị tràn xuống
            bar_height = height  # Giảm bớt 5 pixel để oval không bị đè

            # Vẽ thân bar (hình chữ nhật)
            bar = self.canvas.create_rectangle(x, 150 - bar_height, x + 15, 150, fill="#03B0C4", outline="")

            # Vẽ đầu bo tròn (hình oval)
            radius = 10  # Điều chỉnh độ bo tròn
            oval = self.canvas.create_oval(x, 150 - bar_height - radius, x + 15, 150 - bar_height + radius - 1, fill="#03B0C4", outline="")

            self.bars.append((bar, oval))  # Lưu cả 2 phần để cập nhật sau

    def update_random_spectrogram(self):
        for i, (bar, oval) in enumerate(self.bars):
            new_height = random.randint(20, 120)
            
            # Giảm chiều cao bar để tránh oval bị tràn vào
            bar_height = new_height - 5

            # Cập nhật vị trí của thân bar
            self.canvas.coords(bar, 20 + i * 35, 150 - bar_height, 35 + i * 35, 150)

            # Cập nhật vị trí của oval
            radius = 7
            self.canvas.coords(oval, 20 + i * 35, 150 - bar_height - radius, 35 + i * 35, 150 - bar_height + radius - 1)

        self.root.after(500, self.update_random_spectrogram)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if file_path:
            self.view_model.select_file(file_path)

    def setting_volume(self, event=None):
        """Cập nhật âm lượng khi user điều chỉnh slider"""
        new_volume = round(float(self.vol_slider.get()), 2)
        self.view_model.setting_volume(new_volume)
        
        if not hasattr(self, "_updating_slider"):
            self.update_volume_icon()

    def load_image_icon(self, path, size):
        img = Image.open(path)
        img = img.resize(size, Image.LANCZOS)  # Resize bằng LANCZOS để giữ chất lượng
        return ImageTk.PhotoImage(img)

    def update_buttons(self):
        """Cập nhật UI dựa trên trạng thái hiện tại"""
        state = self.view_model.model.get_state()
        print("State:", state)

        # Xóa tất cả button hiện có
        for widget in self.button_frame.winfo_children():
            widget.grid_forget()

        # Hiển thị button phù hợp với trạng thái
        if state == AudioPlayerState.STOPPED:
            self.play_button = ttk.Button(self.button_frame, image=self.play_icon, bootstyle="dark-link", command=self.view_model.play_command, )    
            self.play_button.grid(row=0, column=0, padx=13)
        elif state == AudioPlayerState.PLAYING:
            self.pause_button = ttk.Button(self.button_frame, image=self.pause_icon, bootstyle="dark-link", command=self.view_model.pause_command)
            self.pause_button.grid(row=0, column=0, padx=13)
        elif state == AudioPlayerState.PAUSED:
            self.resume_button = ttk.Button(self.button_frame, image=self.resume_icon, bootstyle="dark-link", command=self.view_model.unpause_command)
            self.resume_button.grid(row=0, column=0, padx=13)

        self.stop_button = ttk.Button(self.button_frame, image=self.stop_icon, bootstyle="dark-link", command=self.view_model.stop_command)
        self.stop_button.grid(row=0, column=1, padx=13)     
        if state == AudioPlayerState.RECORDING:
            self.stop_voice_button = ttk.Button(self.button_frame, image=self.stop_voice, bootstyle="dark-link", command=self.view_model.stop_command)
            self.stop_voice_button.grid(row=0, column=3, padx=5)
        else:
            self.voice_button = ttk.Button(self.button_frame, image=self.voice, bootstyle="dark-link", command=self.view_model.voice_command)
            self.voice_button.grid(row=0, column=3, padx=5)

    # Seek
    def update_progress(self):
        pass

    def seek_audio(self, value):
        pass

    def toggle_mute(self):
        """Mute hoặc restore volume khi click vào icon"""
        self.view_model.toggle_mute()
        self.update_volume_icon()

    def update_volume_icon(self):
        """Cập nhật icon volume hoặc mute"""
        self._updating_slider = True

        if self.view_model.model.muted:
            self.vol_button.config(image=self.mute_icon)
            self.vol_slider.set(0)
        else:
            volume = float(self.view_model.model.volume)
            self.vol_button.config(image=self.volume_icon)
            self.vol_slider.set(volume)

        self._updating_slider = False  # Bật lại sự kiện sau khi cập nhật