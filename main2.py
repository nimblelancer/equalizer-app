import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from views.ttkbootstrap.main_view import Mainview

if __name__ == "__main__":
    # Khởi tạo ttkbootstrap root và Model, View, ViewModel
    root = ttk.Window(themename="superhero")  # Chọn theme phù hợp
    root.geometry("900x600")
    root.resizable(False, False)

    
    
    root.grid_rowconfigure(0, weight=1)  # Cho phép hàng mở rộng
    root.grid_columnconfigure(0, weight=1)  # Cột trái mở rộng
    root.grid_columnconfigure(1, weight=2)  # Cột giữa (AudioPlayerView) mở rộng nhiều hơn
    root.grid_columnconfigure(2, weight=1)  # Cột phải mở rộng

    main_view = Mainview(root)

    root.mainloop()
