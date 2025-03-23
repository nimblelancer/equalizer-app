import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class FilterFreqResponseGraphView:
    def __init__(self, parent, view_model):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)  # Tạo canvas cho đồ thị
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.view_model = view_model
        self.setup_axs()

    def setup_axs(self):
        self.ax.clear()
        f, hs = self.view_model.get_frequency_response()
        for h in hs:
            self.ax.semilogx(f, 20 * np.log10(abs(h)))

        # Cài đặt tiêu đề và nhãn
        self.ax.set_title('Đáp ứng tần số - Các Bộ Lọc (Peaking, Shelving, Highpass, Lowpass)')
        self.ax.set_xlabel('Tần số (Hz)')
        self.ax.set_ylabel('Độ lớn (dB)')
        self.ax.grid(True)
        self.ax.set_ylim([-30, 30])  # Giới hạn trục y từ -30 dB đến 30 dB

        # Thêm dấu mốc tần số
        xticks = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
        self.ax.set_xticks(xticks)
        self.ax.set_xticklabels(['20', '50', '100', '200', '500', '1k', '2k', '5k', '10k', '20k'])

    def update_graph(self):
        """Cập nhật đồ thị khi có sự thay đổi trong dữ liệu của view model"""
        self.setup_axs()
        self.canvas.draw()
