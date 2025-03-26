import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from views.ttkbootstrap.main_view import Mainview

if __name__ == "__main__":
    # Khởi tạo ttkbootstrap root và Model, View, ViewModel
    root = ttk.Window()  # Chọn theme phù hợp
    root.geometry("600x900")
    root.resizable(False, False)

    style = ttk.Style()
    style.load_user_themes("custom.json")
    style.theme_use("mytheme")
    
    root.grid_rowconfigure(0, weight=1)  # Hàng đầu tiên mở rộng
    root.grid_rowconfigure(1, weight=2)  # Hàng thứ hai mở rộng hơn
    root.grid_rowconfigure(2, weight=1)  # Hàng cuối cùng mở rộng

    root.grid_columnconfigure(0, weight=1)  # Cột chính, căn giữa nội dung

    main_view = Mainview(root)

    root.mainloop()
