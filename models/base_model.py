import threading
import queue

class G2BaseModel:
    def __init__(self):
        self.listeners = {}  # Lưu trữ listeners cho mỗi sự kiện riêng biệt

        self.event_queue = queue.Queue()
        self.stop_thread_event = threading.Event()
        self.notify_thread = threading.Thread(target=self._process_notifications)
        self.notify_thread.start()

    def add_listener(self, event_name, listener):
        """Đăng ký listener cho một sự kiện cụ thể"""
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        if listener not in self.listeners[event_name]:
            self.listeners[event_name].append(listener)

    def remove_listener(self, event_name, listener):
        """Xóa listener khỏi sự kiện cụ thể"""
        if event_name in self.listeners and listener in self.listeners[event_name]:
            self.listeners[event_name].remove(listener)

    def notify(self, event_name, data_dict):
        """Gửi thông báo đến tất cả các listeners của một sự kiện cụ thể"""
        if event_name in self.listeners:
            for listener in self.listeners[event_name]:
                listener.on_notify(event_name, data_dict)

    def notify_queued(self, event_name, data):
        """Thông báo cho tất cả các listener đã đăng ký với sự kiện"""
        self.event_queue.put((event_name, data))

    def _process_notifications(self):
        """Dành riêng cho việc xử lý các thông báo trong một thread khác"""
        while not self.stop_thread_event.is_set():  # Kiểm tra sự kiện dừng thread
            try:
                event_name, data = self.event_queue.get(timeout=1)  # Thêm timeout để tránh block lâu
                self.notify(event_name, data)
            except queue.Empty:
                continue

    def on_close(self):
        """Phương thức này dừng thread một cách an toàn"""
        self.stop_thread_event.set()  # Đặt sự kiện dừng thread
        self.notify_thread.join()  # Đảm bảo thread đã dừng
        print("thread on model closed")