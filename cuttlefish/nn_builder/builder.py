from cuttlefish.nn.configs import configuration_loader
from cuttlefish.utils import aws

import os


def run(application_context):

    ecs_cluster_name = application_context.aws_config.get('cluster')
    task_definition = application_context.aws_config.get('task_definition')
    total_number_of_nodes = application_context.total_nodes

    print("...Spinning up node instances (docker containers) in ECS cluster: {0}".format(ecs_cluster_name))

    success = aws.create_new_ecs_task_instances(ecs_cluster_name, task_definition, total_number_of_nodes)
    print("...Instances created successful: {0}".format(success))

    return success


def calculate_number_nodes(num_hidden_layers, num_nodes_per_layer, num_parameter_servers):

    return (num_hidden_layers * num_nodes_per_layer) + num_parameter_servers


def get_configuration_dir():
    """
    Get the configuration directory for the application.
    :return: string of the path of the configuration directory
    """

    return build_abs_path_config_path('../nn/configs/')


def build_abs_path_config_path(config_path):
    """
        Builds path to given a given configuration file or directory.
        :param config_path:
        :return: path
    """

    here = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(here, config_path)

    return path


def load_nn_config(config_file):
    """
        Loads the neural network yaml file
        :param config_file: path to file
        :return: dictionary of corresponding yaml
    """

    nn_yaml_config = _load_yaml_configuration(config_file)

    if not nn_yaml_config or not isinstance(nn_yaml_config, dict) and not "neuralnetwork" in nn_yaml_config and not "training" in nn_yaml_config and not "ecs" in nn_yaml_config :
        raise Exception('Invalid configuration.  Expected sections are missing.')

    return nn_yaml_config


def _load_yaml_configuration(config_file):
    """
        Loads yaml configuration file of a given name and path.
        :return: Python object that represents the yaml
    """

    if not config_file or not isinstance(config_file, str):
        raise Exception('config_file is invalid, it must be a string and can\'t be empty or None.')

    config_loader = configuration_loader.ConfigurationLoader(config_file)
    return config_loader.load_config()


