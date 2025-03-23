import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# from audio_service import AudioService
from core.player.equalizer_service2 import EqualizerService2
from models.audio_player_model import AudioPlayerModel
from views.audio_player_view import AudioPlayerView
from viewmodels.audio_player_viewmodel import AudioPlayerViewModel
from views.equalizer_view import EqualizerView
from viewmodels.equalizer_advanced_viewmodel import EqualizerViewModel2
from core.player.pyaudio_audio_stream import PyAudioStreamWrapper
from views.audio_graph_view2 import AudioGraphView2
from viewmodels.audio_graph_viewmodel import AudioGraphViewModel
from models.equalizer_model import EqualizerModel

if __name__ == "__main__":
    # Khởi tạo ttkbootstrap root và Model, View, ViewModel
    root = ttk.Window(themename="darkly")  # Chọn theme phù hợp

    # Khởi tạo các thành phần
    equalizer_svc = EqualizerService2()
    equalizer_model = EqualizerModel(equalizer_svc)
    audio_model = AudioPlayerModel(PyAudioStreamWrapper, equalizer_svc)
    player_viewmodel = AudioPlayerViewModel(audio_model)
    player_view = AudioPlayerView(root, player_viewmodel)

    equalizer_viewmodel = EqualizerViewModel2(equalizer_model)
    equalizer_view = EqualizerView(root, equalizer_viewmodel)
    equalizer_view.pack(pady=20)

    # audio_graph_viewmodel = AudioGraphViewModel(audio_model)
    # audio_graph_view = AudioGraphView2(root, audio_graph_viewmodel)
    # audio_graph_view.pack(pady=20)

    # Bắt đầu vòng lặp giao diện người dùng
    root.mainloop()