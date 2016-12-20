

class ApplicationContext(object):

    def __init__(self, nn_config, training_config, aws_config):

        self.nn_config = nn_config
        self.training_config = training_config
        self.aws_config = aws_config