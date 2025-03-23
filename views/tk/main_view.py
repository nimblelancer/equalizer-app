import tkinter as tk
from di_container import DiContainer
from views.audio_player_view2 import AudioPlayerView2
from views.equalizer_view import EqualizerView
from views.audio_graph_view2 import AudioGraphView2
from views.equalizer_view2 import EqualizerView2
# from views.tkinter.subview2 import SubView2

class Mainview:
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title("Main View")

        self.container = DiContainer()

        self.audio_player_view = AudioPlayerView2(root, self.container.audio_player_viewmodel())
        self.audio_player_view.pack()

        self.basic_equalizer_view = EqualizerView(root, self.container.basic_equalizer_viewmodel())
        self.basic_equalizer_view.pack()

        self.button1 = tk.Button(root, text="Advance Setting", command=self.advanced_setting)
        self.button1.pack(side=LEFT, padx=5)

        self.button2 = tk.Button(root, text="Show Graph", command=self.show_graph)
        self.button2.pack(side=LEFT, padx=5)

    def show_graph(self):
        audio_graph_window = Toplevel(self.root)
        AudioGraphView2(audio_graph_window, self.container.audio_graphs_viewmodel())

    def advanced_setting(self): 
        eq_setting_window = tk.Toplevel(self.root)
        EqualizerView2(eq_setting_window, self.container.advanced_equalizer_viewmodel())