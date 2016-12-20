

class ApplicationContext(object):

    def __init__(self, nn_config, training_config, aws_config, total_nodes, instance_ip_addresses=None):

        self.nn_config = nn_config
        self.training_config = training_config
        self.aws_config = aws_config
        self.total_nodes = total_nodes
        self.instance_ip_addresses = instance_ip_addresses
