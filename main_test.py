import ttkbootstrap as tb
import random
import tkinter as tk
from ttkbootstrap.constants import *
from tkinter import filedialog, PhotoImage
from viewmodels.audio_player_viewmodel import AudioPlayerViewModel
from viewmodels.audio_graph_viewmodel import AudioGraphViewModel

class EqualizerAudioPlayerApp(tb.Frame):
    def __init__(self, root, view_model: AudioPlayerViewModel):
        super().__init__(root)
        self.root = root
        self.view_model = view_model
        self.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Ảnh nền nốt nhạc
        self.note_image = PhotoImage(file="assets/mp_background.png").subsample(2, 2)
        self.image_label = tb.Label(self, image=self.note_image)
        self.image_label.pack(pady=5)

        # Frame chứa các preset
        self.preset_frame = tb.Frame(self, bootstyle="dark")
        self.preset_frame.pack(pady=5)
        presets = ["Custom", "Normal", "Pop", "Classic", "Heavy M"]
        for preset in presets:
            btn = tb.Button(self.preset_frame, text=preset, bootstyle="secondary", padding=(5, 2))
            btn.pack(side="left", padx=5)

        # Canvas Equalizer
        self.canvas = tk.Canvas(self, width=550, height=150, bg="#121212", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.bars = []
        self.draw_equalizer()
        self.update_equalizer()

        # Bass & 3D Effect
        self.bass_label = tb.Label(self, text="Bass Boost: 23%", bootstyle="light", background="#121212")
        self.bass_label.pack()
        self.bass_slider = tb.Scale(self, from_=0, to=100, bootstyle="primary", orient="horizontal", command=self.update_bass)
        self.bass_slider.set(23)
        self.bass_slider.pack(pady=5)

        self.effect_label = tb.Label(self, text="3D Effect: 69%", bootstyle="light", background="#121212")
        self.effect_label.pack()
        self.effect_slider = tb.Scale(self, from_=0, to=100, bootstyle="primary", orient="horizontal", command=self.update_effect)
        self.effect_slider.set(69)
        self.effect_slider.pack(pady=5)

        # Frame chứa nút điều khiển
        self.button_frame = tb.Frame(self)
        self.button_frame.pack(pady=10)

        self.play_icon = PhotoImage(file="assets/play.png").subsample(13, 13)
        self.stop_icon = PhotoImage(file="assets/stop.png").subsample(13, 13)
        self.pause_icon = PhotoImage(file="assets/pause.png").subsample(13, 13)
        self.resume_icon = PhotoImage(file="assets/resume.png").subsample(13, 13)

        self.play_button = tb.Button(self.button_frame, image=self.play_icon, command=view_model.play_command)
        self.play_button.pack(side=LEFT, padx=5)
        self.stop_button = tb.Button(self.button_frame, image=self.stop_icon, command=view_model.stop_command)
        self.stop_button.pack(side=LEFT, padx=5)
        self.pause_button = tb.Button(self.button_frame, image=self.pause_icon, command=view_model.pause_command)
        self.pause_button.pack(side=LEFT, padx=5)
        self.unpause_button = tb.Button(self.button_frame, image=self.resume_icon, command=view_model.unpause_command)
        self.unpause_button.pack(side=LEFT, padx=5)

        self.select_file_button = tb.Button(self, text="Select File", command=self.select_file, bootstyle="info outline")
        self.select_file_button.pack(pady=5)

        # Thanh trượt âm lượng
        self.vol_frame = tb.Frame(self)
        self.vol_frame.pack(pady=10)
        tb.Label(self.vol_frame, text="Volume").pack(side=LEFT, padx=10)
        self.vol_slider = tb.Scale(self.vol_frame, from_=0, to=5, orient="horizontal", command=self.setting_volume)
        self.vol_slider.pack(side=LEFT, padx=10)
        self.vol_slider.set(1)

        self.view_model.add_view_listener(self)

    def draw_equalizer(self):
        self.canvas.delete("all")
        for i in range(15):
            x = 20 + i * 35
            height = random.randint(20, 100)
            bar = self.canvas.create_rectangle(x, 150 - height, x + 15, 150, fill="#00D8FF", outline="")
            self.bars.append(bar)

    def update_equalizer(self):
        for i, bar in enumerate(self.bars):
            new_height = random.randint(20, 120)
            self.canvas.coords(bar, 20 + i * 35, 150 - new_height, 35 + i * 35, 150)
        self.root.after(500, self.update_equalizer)

    def update_bass(self, value):
        self.bass_label.config(text=f"Bass Boost: {int(float(value))}%")

    def update_effect(self, value):
        self.effect_label.config(text=f"3D Effect: {int(float(value))}%")

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if file_path:
            self.view_model.set_file_audio(file_path)

    def setting_volume(self, event=None):
        self.view_model.setting_volume(round(float(self.vol_slider.get()), 1))

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    view_model = AudioPlayerViewModel()
    app = EqualizerAudioPlayerApp(root, view_model)
    root.mainloop()