import tkinter as tk
from tkinter import filedialog
from viewmodels.audio_player_viewmodel import AudioPlayerViewModel
from views.audio_graph_view2 import AudioGraphView2
from viewmodels.audio_graph_viewmodel import AudioGraphViewModel
from tkinter import Toplevel

class AudioPlayerView:
    def __init__(self, root, view_model: AudioPlayerViewModel):
        self.root = root
        self.root.title("Audio Player")
        
        # Tạo một frame chứa các button
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        # Tạo các nút điều khiển
        self.play_button = tk.Button(self.button_frame, text="Play", width=10, command=view_model.play_command)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.button_frame, text="Stop", width=10, command=view_model.stop_command)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(self.button_frame, text="Pause", width=10, command=view_model.pause_command)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.unpause_button = tk.Button(self.button_frame, text="Unpause", width=10, command=view_model.unpause_command)
        self.unpause_button.pack(side=tk.LEFT, padx=5)

        self.select_file_button = tk.Button(self.button_frame, text="Select File", width=10, command=self.select_file)
        self.select_file_button.pack(side=tk.LEFT, padx=5)

        self.voice_button = tk.Button(self.button_frame, text="Voice", width=10, command=view_model.voice_command)
        self.voice_button.pack(side=tk.LEFT, padx=5)

        self.vol_slider = tk.Scale(self.button_frame, from_=0, to=5, resolution=0.1, orient="horizontal", command=self.setting_volume)
        self.vol_slider.pack(side=tk.LEFT, padx=5)
        self.vol_slider.set(1)

        self.voice_button = tk.Button(self.button_frame, text="Graph", width=10, command=self.show_graph)
        self.voice_button.pack(side=tk.LEFT, padx=5)

        self.selected_file = ""  # Biến lưu trữ đường dẫn tệp được chọn
        self.view_model = view_model
        
        self.view_model.add_view_listener(self)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if file_path:
            self.view_model.set_file_audio(file_path)

    def show_graph(self):
        # Tạo cửa sổ con mới
        new_window = Toplevel(self.root)  # 'root' là cửa sổ chính
        new_window.title("Graph views")

        graph_viewmodel = AudioGraphViewModel(self.view_model.model)
        
        graph_view = AudioGraphView2(new_window, graph_viewmodel)

    def setting_volume(self, event=None):
        self.view_model.setting_volume(self.vol_slider.get())

    def update_view(self, event_name, data):
        """Phương thức sẽ được gọi khi ViewModel thay đổi"""
        print("AudioPlayerView update_view:", event_name, data)
        # is_playing = self.view_model.get_property("is_playing")
        # selected_file = self.view_model.get_property("selected_file")

        # # Cập nhật giao diện người dùng khi trạng thái thay đổi
        # if is_playing:
        #     print("Audio is playing")
        # else:
        #     print("Audio is stopped or paused")

        # print(f"Selected file: {selected_file}")
