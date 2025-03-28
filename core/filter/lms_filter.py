import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

class LMSFilter:
    def __init__(self, mu, N, r):
        """
        :param mu: Tốc độ học (learning rate)
        :param N: Kích thước bộ lọc (filter size)
        :param r: Tín hiệu tham chiếu nhiễu (reference noise)
        """
        self.mu = mu  # Tốc độ học
        self.N = N  # Kích thước bộ lọc
        self.r = r  # Tín hiệu tham chiếu nhiễu
        self.weights = np.zeros(N)  # Trọng số của bộ lọc (bắt đầu từ 0)
        
    def apply(self, x):
        """
        Áp dụng bộ lọc LMS vào tín hiệu đầu vào x và tín hiệu tham chiếu nhiễu r
        
        :param x: Dữ liệu vào (input signal)
        :return: Tín hiệu đầu ra
        """
        M = len(x)
        print("lenx là ", M)
        print("lenr là ", len(self.r))
        y = np.zeros(M)  # Tín hiệu đầu ra
        e = np.zeros(M)  # Lỗi (error)
        
        # Duyệt qua tất cả các mẫu
        for n in range(self.N, M):
            # Cửa sổ dữ liệu đầu vào x[n-N+1] đến x[n]
            x_n = x[n-self.N+1:n+1]
            
            # Tín hiệu đầu ra (sử dụng trọng số hiện tại)
            y[n] = np.dot(self.weights, x_n)
            
            # Tính lỗi (Lỗi giữa tín hiệu đầu ra và tín hiệu tham chiếu)
            e[n] = self.r[n] - y[n]
            
            # Kiểm tra NaN hoặc vô cùng trong lỗi và đầu vào
            if np.any(np.isnan(e[n])) or np.any(np.isinf(e[n])) or np.any(np.isnan(x_n)) or np.any(np.isinf(x_n)):
                # print(f"NaN hoặc vô cùng phát hiện tại n = {n}")
                # print(f"e[{n}] = {e[n]}")
                # print(f"y_n = {y[n]}")
                continue  # Bỏ qua cập nhật trọng số nếu có lỗi
            
            # Cập nhật trọng số
            self.weights += 2 * self.mu * e[n] * x_n  # Cập nhật LMS
        
        return y
