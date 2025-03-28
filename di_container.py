from dependency_injector import containers, providers
from models.audio_player_model import AudioPlayerModel
from models.equalizer_model import EqualizerModel
from viewmodels.audio_player_viewmodel import AudioPlayerViewModel
from viewmodels.equalizer_basic_viewmodel import EqualizerBasicViewModel
from viewmodels.equalizer_advanced_viewmodel import EqualizerAdvancedViewModel
from viewmodels.audio_graph_viewmodel import AudioGraphViewModel
from viewmodels.noise_suppression_viewmodel import NoiseSuppressionViewModel
from core.player.equalizer_service2 import EqualizerService2
from core.player.noise_suppression_service import NoiseSuppressionService
from core.player.pyaudio_audio_stream import PyAudioStreamWrapper
from config_manager import ConfigManager
from viewmodels.noise_suppression_viewmodel import NoiseSuppressionViewModel

class DiContainer(containers.DeclarativeContainer):
    # Khởi tạo config manager
    config_manager = providers.Singleton(ConfigManager, config_file="config.ini")
    # Khởi tạo core
    equalizer_svc = providers.Singleton(EqualizerService2)
    noise_suppress_svc = providers.Singleton(NoiseSuppressionService)

    # Khởi tạo model
    audio_player_model = providers.Singleton(AudioPlayerModel, audio_stream_class=PyAudioStreamWrapper, eq_service=equalizer_svc, noise_service=noise_suppress_svc, config_manager=config_manager)
    equalizer_model = providers.Singleton(EqualizerModel, eq_service=equalizer_svc, noise_service=noise_suppress_svc, config_manager=config_manager)
    
    # Khởi tạo viewmodel
    audio_player_viewmodel = providers.Factory(AudioPlayerViewModel, model=audio_player_model)
    basic_equalizer_viewmodel = providers.Factory(EqualizerBasicViewModel, model=equalizer_model)
    advanced_equalizer_viewmodel = providers.Factory(EqualizerAdvancedViewModel, model=equalizer_model)
    audio_graphs_viewmodel = providers.Factory(AudioGraphViewModel, model=audio_player_model)
    audio_noise_viewmodel = providers.Factory(NoiseSuppressionViewModel, model=equalizer_model)