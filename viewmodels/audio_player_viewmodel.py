from tkinter import filedialog
from base.base_command import G2Command
from base.base_viewmodel import G2BaseViewModel
from models.audio_player_model import AudioPlayerModel
from views.audio_player_view import AudioPlayerView
from models.audio_player_model import AudioPlayerState

class AudioPlayerViewModel (G2BaseViewModel):
    def __init__(self, model: AudioPlayerModel, view: None):

        super().__init__(model)
        self.model = model
        self.view = view
        self.model.add_listener("player_changed", self)
        self.model.set_progress_callback(self.update_ui_from_model)
        self.is_seeking = False

    def set_view(self, view):
        """Phương thức để gán view sau khi ViewModel đã được khởi tạo"""
        self.view = view

    def play_audio(self):
        """Khi nút Play được nhấn"""
        state = self.model.get_state()
        
        if state == AudioPlayerState.STOPPED:
            # Bắt đầu phát nếu đang dừng
            self.model.play_audio()
        elif state == AudioPlayerState.PAUSED:
            # Tiếp tục phát nếu đang tạm dừng
            self.model.unpause_audio()

    def stop_audio(self):
        """Khi nút Stop được nhấn"""
        self.model.stop_audio()
        # Reset thanh tiến trình về 0
        self.view.scale.set(0)
        self.view.elapse_label.config(text="00:00")
        self.view.remain_label.config(text=self.model.format_time(self.model.duration) if self.model.duration > 0 else "00:00")

    def pause_audio(self):
        """Khi nút Pause được nhấn"""
        if self.model.get_state() == AudioPlayerState.PLAYING:
            self.model.pause_audio()

    def unpause_audio(self):
        """Khi nút Unpause được nhấn"""
        self.model.unpause_audio()

    def select_file(self):
        """Khi nút Select File được nhấn"""
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if file_path:
            self.model.selected_file = file_path
            self.model.play_audio()

    def voice_action(self):
        """Khi nút Voice được nhấn"""
        self.model.start_voice()

    def setting_volume(self, value):
        """Xử lý khi thay đổi Volume"""
        self.model.volume = int(float(value))

    def on_progress(self, val):
        """
        Xử lý khi người dùng tương tác với thanh tiến trình
        Được gọi từ Scale widget trong View
        """
        # Đánh dấu đang trong quá trình kéo thanh tiến trình
        self.is_seeking = True
        
        # Cập nhật vị trí hiện tại dựa trên giá trị thanh trượt
        percentage = float(val)
        
        # Tính thời gian dựa trên phần trăm
        total_seconds = self.model.duration
        elapsed = (percentage / 100) * total_seconds
        remaining = max(0, total_seconds - elapsed)
        
        # Cập nhật nhãn thời gian trên giao diện
        self.view.elapse_label.config(text=self.model.format_time(elapsed))
        self.view.remain_label.config(text=self.model.format_time(remaining))

    def on_progress_release(self, event):
        """
        Xử lý khi người dùng thả chuột sau khi kéo thanh tiến trình
        Cần được gọi từ View khi có sự kiện ButtonRelease trên Scale
        """
        if self.is_seeking:
            # Lấy giá trị cuối cùng của thanh trượt
            percentage = float(self.view.scale.get())
            
            # Gửi đến model để cập nhật vị trí phát
            self.model.seek_to_position(percentage)
            
            # Đánh dấu đã kết thúc kéo
            self.is_seeking = False

    def update_ui_from_model(self, percentage):
        """
        Cập nhật UI dựa trên tiến trình từ model
        Được gọi thông qua callback từ model
        """
        # Chỉ cập nhật UI nếu người dùng không đang kéo thanh trượt
        if not self.is_seeking:
            # Cập nhật giá trị thanh trượt
            self.view.scale.set(percentage)
            
            # Cập nhật nhãn thời gian
            elapsed = self.model.elapsed_var
            remaining = self.model.remain_var
            
            self.view.elapse_label.config(text=self.model.format_time(elapsed))
            self.view.remain_label.config(text=self.model.format_time(remaining))