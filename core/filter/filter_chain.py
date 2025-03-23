class FilterChain:
    def __init__(self):
        self.filters = []

    def reset_filter(self):
        """Xóa tất cả bộ lọc trong chuỗi."""
        self.filters.clear()

    def is_empty(self):
        return len(self.filters) == 0

    def add_filter(self, filter_obj, priority=0):
        """Thêm bộ lọc vào chuỗi với một mức độ ưu tiên."""
        self.filters.append((filter_obj, priority))
        # Sắp xếp các bộ lọc theo ưu tiên (priority) từ cao xuống thấp
        self.filters.sort(key=lambda x: x[1], reverse=True)

    def apply(self, audio_data):
        """Áp dụng tất cả bộ lọc lên tín hiệu âm thanh."""
        for filter_obj, _ in self.filters:
            audio_data = filter_obj.apply(audio_data)
        return audio_data
    
    def get_coefficients(self):
        """Trả về danh sách các hệ số a và b của tất cả các bộ lọc trong chuỗi."""
        filter_coefs = []
        
        for filter, _ in self.filters:
            # Lấy hệ số b và a của bộ lọc
            b, a = filter.get_coefficients()
            filter_coefs.append({'b': b, 'a': a})

        return filter_coefs
        