# equalizer_advance_view.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class EqualizerAdvanceView(ttk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Equalizer Advanced Settings")
        self.geometry("300x250")
        self.resizable(False, False)
        
        ttk.Label(self, text="Preset Settings", font=("Arial", 12, "bold")).pack(pady=10)
        
        presets = ["Flat", "Rock", "Pop", "Jazz", "Classical", "Custom"]
        for preset in presets:
            btn = ttk.Button(self, text=preset, width=20, command=lambda p=preset: self.select_preset(p))
            btn.pack(pady=5)
        
        ttk.Button(self, text="Close", bootstyle=SECONDARY, command=self.destroy).pack(pady=10)
    
    def select_preset(self, preset):
        # Ở đây bạn có thể gắn thêm logic cho preset (apply preset về EQ chính)
        print(f"Selected preset: {preset}")
        # Tạm thời chỉ print ra preset đã chọn
