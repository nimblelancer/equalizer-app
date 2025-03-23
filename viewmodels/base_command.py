class G2Command:
    def __init__(self, execute, can_execute=None):
        self.execute = execute  # Phương thức thực thi hành động
        self.can_execute = can_execute if can_execute else lambda: True  # Kiểm tra xem hành động có thể thực thi hay không
    
    def __call__(self):
        if self.can_execute():
            self.execute()
