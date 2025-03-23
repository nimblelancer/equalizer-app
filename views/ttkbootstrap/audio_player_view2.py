import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, PhotoImage
from viewmodels.audio_player_viewmodel import AudioPlayerViewModel
# from views.audio_graph_view2 import AudioGraphView2
from viewmodels.audio_graph_viewmodel import AudioGraphViewModel
from tkinter import Toplevel

class AudioPlayerView2(ttk.Frame):
    def __init__(self, root, view_model: AudioPlayerViewModel):
        super().__init__(root)
        self.view_model = view_model
        self.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Ảnh nền nốt nhạc
        self.note_image = PhotoImage(file="assets/mp_background.png").subsample(2,2)
        self.image_label = ttk.Label(self, image=self.note_image)
        self.image_label.pack(pady=5)

        # Frame chứa nút điều khiển
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=10)

        # Load icon với kích thước nhỏ hơn
        self.play_icon = PhotoImage(file="assets/play.png").subsample(13,13)
        self.stop_icon = PhotoImage(file="assets/stop.png").subsample(13,13)
        self.pause_icon = PhotoImage(file="assets/pause.png").subsample(13,13)
        self.resume_icon = PhotoImage(file="assets/resume.png").subsample(13,13)

        # Các nút điều khiển
        self.play_button = ttk.Button(self.button_frame, image=self.play_icon, command=view_model.play_command)
        self.play_button.pack(side=LEFT, padx=5)

        self.stop_button = ttk.Button(self.button_frame, image=self.stop_icon, command=view_model.stop_command)
        self.stop_button.pack(side=LEFT, padx=5)

        self.pause_button = ttk.Button(self.button_frame, image=self.pause_icon, command=view_model.pause_command)
        self.pause_button.pack(side=LEFT, padx=5)

        self.unpause_button = ttk.Button(self.button_frame, image=self.resume_icon, command=view_model.unpause_command)
        self.unpause_button.pack(side=LEFT, padx=5)

        # Nút Graph & Select File
        self.graph_button = ttk.Button(self, text="Graph", command=None, bootstyle="info outline")
        self.graph_button.pack(pady=5)

        self.select_file_button = ttk.Button(self, text="Select File", command=self.select_file, bootstyle="info outline")
        self.select_file_button.pack(pady=5)

        # Thanh trượt âm lượng
        self.vol_frame = ttk.Frame(self)
        self.vol_frame.pack(pady=10)
        ttk.Label(self.vol_frame, text="Volume").pack(side=LEFT, padx=10)
        self.vol_slider = ttk.Scale(self.vol_frame, from_=0, to=5, orient="horizontal", command=self.setting_volume)
        self.vol_slider.pack(side=LEFT, padx=10)
        self.vol_slider.set(1)

        self.view_model.add_view_listener(self)
    
    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if file_path:
            self.view_model.set_file_audio(file_path)
    
    # def show_graph(self):
    #     new_window = Toplevel(self.root)
    #     new_window.title("Graph views")
    #     graph_viewmodel = AudioGraphViewModel(self.view_model.model)
    #     graph_view = AudioGraphView2(new_window, graph_viewmodel)
    
    def setting_volume(self, event=None):
        self.view_model.setting_volume(round(float(self.vol_slider.get()), 1))