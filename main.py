import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# from audio_service import AudioService
from core.player.equalizer_service2 import EqualizerService2
from models.audio_player_model import AudioPlayerModel
from views.audio_player_view_temp import AudioPlayerView
from viewmodels.audio_player_viewmodel import AudioPlayerViewModel
from views.equalizer_view_temp import EqualizerView
from viewmodels.equalizer_advanced_viewmodel import EqualizerViewModel2
from core.player.pyaudio_audio_stream import PyAudioStreamWrapper
from viewmodels.audio_graph_viewmodel import AudioGraphViewModel
from models.equalizer_model import EqualizerModel

if __name__ == "__main__":
    # Khởi tạo ttkbootstrap root và Model, View, ViewModel
    root = ttk.Window(themename="darkly")  # Chọn theme phù hợp
    root.geometry("900x500")
    root.resizable(True, True)

     # Cấu hình layout 2 cột
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # Khởi tạo các thành phần
    equalizer_svc = EqualizerService2()
    equalizer_model = EqualizerModel(equalizer_svc)
    audio_model = AudioPlayerModel(PyAudioStreamWrapper, equalizer_svc)
    player_viewmodel = AudioPlayerViewModel(audio_model)
    player_view = AudioPlayerView(root, player_viewmodel)

    equalizer_viewmodel = EqualizerViewModel2(equalizer_model)
    equalizer_view = EqualizerView(root, equalizer_viewmodel)

    root.mainloop()