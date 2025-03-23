import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from views2.main_view import Mainview

if __name__ == "__main__":
    # Khởi tạo ttkbootstrap root và Model, View, ViewModel
    root = ttk.Window(themename="darkly")  # Chọn theme phù hợp
    root.geometry("900x500")
    root.resizable(True, True)

     # Cấu hình layout 2 cột
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    main_view = Mainview(root)

    root.mainloop()
