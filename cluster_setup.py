from cuttlefish.nn.configs import configuration_loader
from cuttlefish.system_models.application_context import ApplicationContext

import os
import argparse

def run(application_context):
    pass


def get_configuration_dir():
    """
    Get the configuration directory for the application.
    :return: string of the path of the configuration directory
    """

    return build_abs_path_config_path('cuttlefish/nn/configs/')


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


if __name__ == '__main__':

    # set up cmd arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-nn', action='store', dest='nn_yaml_file',  help='File that configures the neural network you want to spin up.')

    # parse arguments
    results = parser.parse_args()
    nn_yaml_file = results.nn_yaml_file

    # todo: create application context object
    # step 1: load yaml
    # step 2: calculate number of ECS task instances needed using hyperparameter values from the yaml
    # step 3: call run tasks (from our library to set up new instances of the task...)

    # step 1: load yaml file
    nn_config_dir = get_configuration_dir()
    nn_config_file = os.path.join(nn_config_dir, nn_yaml_file)
    nn_config = load_nn_config(nn_config_file)

    print(nn_config)

    # step 2: calculate the number ECS task instances needed to run the configured NN
    neural_network_config = nn_config.get('neural_network')
    training_config = nn_config.get('training')
    aws_config = nn_config.get('ecs')

    app_context = ApplicationContext(neural_network_config, training_config, aws_config)

    print(app_context)

    # step 3: spin up!
