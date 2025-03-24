import tkinter as tk
from di_container import DiContainer
from views.tk.audio_player_view2 import AudioPlayerView2
from views.tk.equalizer_basic_view import EqualizerBasicView
from views.tk.audio_graph_view import AudioGraphView
from views.tk.equalizer_advanced_view import EqualizerAdvancedView

class Mainview:
    def __init__(self, root):
        self.root = root
        self.root.title("Main View")

        self.container = DiContainer()

        self.audio_player_view = AudioPlayerView2(root, self.container.audio_player_viewmodel())
        self.audio_player_view.pack()

        self.basic_equalizer_view = EqualizerBasicView(root, self.container.basic_equalizer_viewmodel())
        self.basic_equalizer_view.pack()

        self.button1 = tk.Button(root, text="Advance Setting", command=self.advanced_setting)
        self.button1.pack(side=tk.LEFT, padx=5)

        self.button2 = tk.Button(root, text="Show Graph", command=self.show_graph)
        self.button2.pack(side=tk.LEFT, padx=5)

    def show_graph(self):
        audio_graph_window = tk.Toplevel(self.root)
        AudioGraphView(audio_graph_window, self.container.audio_graphs_viewmodel())

    def advanced_setting(self):
        eq_setting_window = tk.Toplevel(self.root)
        EqualizerAdvancedView(eq_setting_window, self.container.advanced_equalizer_viewmodel())