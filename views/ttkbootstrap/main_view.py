import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Toplevel
from di_container import DiContainer
from views.ttkbootstrap.audio_player_view import AudioPlayerView
from views.ttkbootstrap.equalizer_basic_view import EqualizerBasicView
import threading
from views.ttkbootstrap.audio_graph_view import AudioGraphView
from views.ttkbootstrap.equalizer_advanced_view import EqualizerAdvancedView
# from views.tkinter.subview2 import SubView2

class Mainview:
    def __init__(self, root):
        self.root = root
        self.root.title("Main View")

        self.container = DiContainer()

        self.audio_player_view = AudioPlayerView(root, self.container.audio_player_viewmodel())
        self.audio_player_view.grid(row=0, column=0, pady=5, sticky="nsew")  # Căn giữa toàn bộ

        self.basic_equalizer_view = EqualizerBasicView(root, self.container.basic_equalizer_viewmodel())
        self.basic_equalizer_view.grid(row=1, column=0, pady=5, sticky="nsew")  # Căn giữa toàn bộ

        self.additional_setting_btn = ttk.Frame()
        self.additional_setting_btn.grid(row=2, column=0, columnspan=1, padx=10, pady=10)

        self.advance_setting_btn = ttk.Button(self.additional_setting_btn, text="Advance Setting", command=self.advanced_setting)
        self.advance_setting_btn.grid(row=0, column=0, columnspan=1,  padx=10)

        self.show_graph_btn = ttk.Button(self.additional_setting_btn, text="Show Graph", command=self.show_graph)
        self.show_graph_btn.grid(row=0, column=1, columnspan=1, padx=10)

        root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def on_close(self):
        print("Closing application...")
        print(f"Number of threads currently active: {threading.active_count()}")
        self.audio_player_view.on_close()
        self.basic_equalizer_view.on_close()
        
        # Hủy bỏ vòng lặp chính sau 1 ms
        self.root.after(1, self.root.quit)
        self.root.after(1, self.root.destroy)

        print(f"Number of threads remaining: {threading.active_count()}")

    def show_graph(self):
        audio_graph_window = Toplevel(self.root)
        AudioGraphView(audio_graph_window, self.container.audio_graphs_viewmodel())

    def advanced_setting(self):
        eq_setting_window = Toplevel(self.root)
        EqualizerAdvancedView(eq_setting_window, self.container.advanced_equalizer_viewmodel())