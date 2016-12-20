import logging
import yaml

class ConfigurationLoader(object):
    def __init__(self, config_file):
        self.config_file = config_file
        self._config = None

    def load_config(self):
        """
            Loads yaml configuration file and returns yaml file contents as python object.
        """

        try:
            if not self._config:
                with open(self.config_file) as f:
                    self._config = yaml.load(f)
                    logging.debug(self._config)
        except Exception as e:
            logging.error(e)
            raise e

        return self._config
