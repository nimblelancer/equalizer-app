import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import filedialog
from models import AudioPlayerModel
from core import EqualizerService, PyAudioStreamWrapper
from viewmodels.audio_player_viewmodel import AudioPlayerViewModel
from views.audio_graph_view import AudioGraphView  # Import GraphView từ file của bạn
from views.audio_player_view import AudioPlayerView  # Import GraphView từ file của bạn
from views.equalizer_view import EqualizerView  # Import GraphView từ file của bạn


class MainApplication(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Audio Player with Equalizer")
        self.geometry("1200x800")
        
        # Tạo layout grid cho toàn bộ ứng dụng
        self.columnconfigure(0, weight=1)  # Cột bên trái - Audio Player
        self.columnconfigure(1, weight=2)  # Cột bên phải - GraphView
        self.rowconfigure(0, weight=1)     # Hàng trên - Player + Graph
        self.rowconfigure(1, weight=1)     # Hàng dưới - Equalizer
        
        # Equalizer service
        equalizer_svc = EqualizerService()
        audio_model = AudioPlayerModel(PyAudioStreamWrapper, equalizer_svc)

        # AudioPlayer
        left_frame = ttk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        audio_player_viewmodel = AudioPlayerViewModel(audio_model, None)
        self.audio_player_view = AudioPlayerView(left_frame, audio_player_viewmodel)
        
        # Tạo GraphView ở cột bên phải
        self.graph_view = AudioGraphView(self, self.style)
        self.graph_view.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)
        
        # Tạo EqualizerView ở hàng dưới, trải dài cả 2 cột
        self.equalizer = EqualizerView(self)
        self.equalizer.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=10, pady=10)
                
        # Kết nối các thành phần
        # self.connect_components()
        
    # def connect_components(self):
    #     """Kết nối các thành phần với nhau"""
    #     # Ví dụ: khi thay đổi equalizer, cập nhật các biểu đồ
    #     self.equalizer.eq_status.trace_add("write", self.update_graphs)
        
    # def update_graphs(self, *args):
    #     """Cập nhật các biểu đồ khi equalizer thay đổi"""
    #     if self.equalizer.eq_status.get():
    #         # Nếu equalizer đang bật, cập nhật các biểu đồ
    #         self.graph_view.update_all_graphs()

# Khởi tạo và chạy ứng dụng
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()