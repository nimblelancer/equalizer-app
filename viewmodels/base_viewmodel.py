class G2BaseViewModel:
    def __init__(self, model):
        self.model = model
        self.view_listeners = []  # Danh sách các listeners (View)
        self.update_callback = None
        
        # Đăng ký mình vào Model như là một listener
        # self.model.add_listener(self)

    def add_view_listener(self, listener):
        """Đăng ký listener (View)"""
        if listener not in self.view_listeners:
            self.view_listeners.append(listener)

    def remove_view_listener(self, listener):
        """Xóa listener"""
        if listener in self.view_listeners:
            self.view_listeners.remove(listener)

    def notify_view(self, event_name, data):
        """Thông báo cho View để cập nhật giao diện"""
        for listener in self.view_listeners:
            listener.update_view(event_name, data)

    def on_notify(self, event_name, data):
        """Nhận cập nhật từ Model và xử lý nếu cần"""
        # Xử lý dữ liệu từ Model (tùy theo logic của bạn)
        self.notify_view(event_name, data)  # Thông báo dữ liệu đã cập nhật cho View

    def on_close(self):
        self.update_callback = None
        self.model.on_close()