import configparser

class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        self.config.read(self.config_file)

    def reload_config(self):
        """Reload the config file to get updated values."""
        self.load_config()

    def getint(self, section, option):
        return self.config.getint(section, option)

    def getfloat(self, section, option):
        return self.config.getfloat(section, option)