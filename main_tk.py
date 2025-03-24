import tkinter as tk
from views.tk.main_view import Mainview

if __name__ == "__main__":
    # Khởi tạo tkinter root và Model, View, ViewModel
    root = tk.Tk()
    
    main_view = Mainview(root)

    root.mainloop()
