import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Toplevel
from di_container import DiContainer
from views.ttkbootstrap.audio_player_view2 import AudioPlayerView2
from views.ttkbootstrap.equalizer_view import EqualizerView
from views.ttkbootstrap.audio_graph_view2 import AudioGraphView2
from views.ttkbootstrap.equalizer_view2 import EqualizerView2
# from views.tkinter.subview2 import SubView2

class Mainview:
    def __init__(self, root):
        self.root = root
        self.root.title("Main View")

        self.container = DiContainer()

        self.audio_player_view = AudioPlayerView2(root, self.container.audio_player_viewmodel())
        self.audio_player_view.grid(row=0, column=0, columnspan=2, pady=5, sticky=W)

        self.basic_equalizer_view = EqualizerView(root, self.container.basic_equalizer_viewmodel())
        self.basic_equalizer_view.grid(row=1, column=0, columnspan=2, pady=5, sticky=W)

        self.button1 = ttk.Button(root, text="Advance Setting", command=self.advanced_setting)
        self.button1.grid(row=2, column=0, columnspan=2, pady=5, sticky=W)

        self.button2 = ttk.Button(root, text="Show Graph", command=self.show_graph)
        self.button2.grid(row=3, column=0, columnspan=2, pady=5, sticky=W)

    def show_graph(self):
        audio_graph_window = Toplevel(self.root)
        AudioGraphView2(audio_graph_window, self.container.audio_graphs_viewmodel())

    def advanced_setting(self):
        eq_setting_window = Toplevel(self.root)
        EqualizerView2(eq_setting_window, self.container.advanced_equalizer_viewmodel())