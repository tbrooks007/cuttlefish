from cuttlefish.system_models.application_context import ApplicationContext
from cuttlefish.nn_builder import builder

import os
import argparse


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

    print("...Loading neural network config file: {0}".format(nn_yaml_file))

    # step 1: load yaml file
    nn_config_dir = builder.get_configuration_dir()
    nn_config_file = os.path.join(nn_config_dir, nn_yaml_file)
    nn_config = builder.load_nn_config(nn_config_file)

    print(nn_config)
    print("...Building application context object")

    # step 2: calculate the number ECS task instances needed to run the configured NN
    neural_network_config = nn_config.get('neural_network')
    training_config = nn_config.get('training')
    aws_config = nn_config.get('ecs')

    app_context = ApplicationContext(neural_network_config, training_config, aws_config)

    # todo eventually will make this more flexible
    num_hidden_layers = neural_network_config.get('num_of_hidden_layers')
    num_nodes_per_layer = neural_network_config.get('num_nodes_per_layer')
    num_parameter_servers = training_config.get('num_parameter_servers')

    print("...Number of neural network nodes (containers) to spin up: {0}".format(8))

    print(app_context)

    # step 3: spin up!