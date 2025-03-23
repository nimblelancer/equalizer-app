from dependency_injector import containers, providers
from models.audio_player_model import AudioPlayerModel
from models.equalizer_model import EqualizerModel
from viewmodels.audio_player_viewmodel import AudioPlayerViewModel
from viewmodels.equalizer_viewmodel import EqualizerViewModel
from viewmodels.equalizer_advanced_viewmodel import EqualizerViewModel2
from viewmodels.audio_graph_viewmodel import AudioGraphViewModel
from core.player.equalizer_service2 import EqualizerService2
from core.player.pyaudio_audio_stream import PyAudioStreamWrapper

class DiContainer(containers.DeclarativeContainer):
    # Khởi tạo core
    equalizer_svc = providers.Singleton(EqualizerService2)

    # Khởi tạo model
    audio_player_model = providers.Factory(AudioPlayerModel, audio_stream_class=PyAudioStreamWrapper, eq_service=equalizer_svc)
    equalizer_model = providers.Factory(EqualizerModel, eq_service=equalizer_svc)
    
    # Khởi tạo viewmodel
    audio_player_viewmodel = providers.Factory(AudioPlayerViewModel, model=audio_player_model)
    basic_equalizer_viewmodel = providers.Factory(EqualizerViewModel, model=equalizer_model)
    advanced_equalizer_viewmodel = providers.Factory(EqualizerViewModel2, model=equalizer_model)
    audio_graphs_viewmodel = providers.Factory(AudioGraphViewModel, model=audio_player_model)