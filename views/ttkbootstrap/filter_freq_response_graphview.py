import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as ttk
from ttkbootstrap import Style

class FilterFreqResponseGraphView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, padx=10, pady=10)

        # Thu nhỏ đồ thị để cân đối bố cục
        self.fig, self.ax = plt.subplots(figsize=(8, 3))  # Giảm kích thước so với 10x6
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)

        self.style = Style()
        self.theme_bg = self.style.colors.get("bg")
        self.theme_fg = self.style.colors.get("fg")
        self.theme_primary = self.style.colors.get("primary")

    def setup_axs(self, f, hs):
        self.ax.clear()
        
        # Chọn màu chính từ theme
        main_color_fg = self.theme_fg
        main_color_bg = self.theme_bg
        theme_primary = self.theme_primary


        for h in hs:
            magnitude = 20 * np.log10(abs(h))  # Chuyển đổi độ lớn sang dB
            
            # 🌈 Thêm hiệu ứng tô màu phía dưới đường đồ thị
            self.ax.fill_between(f, magnitude, -50, color=theme_primary, alpha=0.2)  # Alpha = độ trong suốt
            
            # 🎨 Vẽ đường đồ thị chính
            self.ax.semilogx(f, magnitude, color=theme_primary, linewidth=1.5)  

        # 🔧 Chỉnh màu nền
        self.ax.set_facecolor(main_color_bg)
        self.fig.patch.set_facecolor(main_color_bg)

        # 🔤 Chỉnh font chữ
        font_size = 8
        self.ax.set_title(
            'Đáp ứng tần số - Các Bộ Lọc (Peaking, Shelving, Highpass, Lowpass)', 
            fontsize=10, fontweight='bold', color=main_color_fg
        )
        self.ax.set_xlabel('Tần số (Hz)', fontsize=font_size, color=main_color_fg)
        self.ax.set_ylabel('Độ lớn (dB)', fontsize=font_size, color=main_color_fg)

        # 🔧 Chỉnh màu trục
        self.ax.xaxis.label.set_color(main_color_fg)
        self.ax.yaxis.label.set_color(main_color_fg)
        self.ax.tick_params(axis='both', colors=main_color_fg)
        for spine in ['bottom', 'top', 'left', 'right']:
            self.ax.spines[spine].set_color(main_color_fg)

        # 🔲 Lưới mờ theo theme
        self.ax.grid(True, color=main_color_fg, linestyle='--', linewidth=0.5, alpha=0.3)

        # 🎚 Chỉnh nhãn trục X
        xticks = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
        self.ax.set_xticks(xticks)
        self.ax.set_xticklabels(
            ['20', '50', '100', '200', '500', '1k', '2k', '5k', '10k', '20k'], 
            fontsize=font_size, color=main_color_fg
        )

        self.ax.set_yticks([-15, -10, -5, 0, 5, 10, 15])
        self.ax.set_yticklabels(
            ['-15', '-10', '-5', '0', '5', '10', '15'], 
            fontsize=font_size, color=main_color_fg
        )

        # 🔧 Căn chỉnh để không bị tràn chữ
        self.fig.tight_layout()

    def update_graph(self, f, hs):
        """Cập nhật đồ thị khi có sự thay đổi trong dữ liệu của view model"""
        self.setup_axs(f, hs)
        self.canvas.draw()

    def on_close(self):
        plt.close(self.fig)

class EqualizerAdvancedView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.controls = []
        freq_labels = ["Bass", "Mid-bass", "Midrange", "Upper Mid", "Treble"]
        for i, label in enumerate(freq_labels):
            frame = ttk.LabelFrame(self, text=f"{label}\nFrequency")
            frame.grid(row=0, column=i, padx=15, pady=10, sticky="n")  # Cách nhau ra hơn

            slider_q = ttk.Scale(frame, from_=0.1, to=10, orient="horizontal")
            slider_q.pack(pady=5)

            label_q = ttk.Label(frame, text="Q")
            label_q.pack()

            slider_gain = ttk.Scale(frame, from_=-12, to=12, orient="horizontal")
            slider_gain.pack(pady=5)

            label_gain = ttk.Label(frame, text="Gain (dB)")
            label_gain.pack()

            self.controls.append((slider_q, slider_gain))
        plt.close(self.fig)  # Đảm bảo rằng các figure được đóng khi ứng dụng kết thúc
