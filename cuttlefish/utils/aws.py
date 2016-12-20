import boto3


def get_all_ec2_public_ip_addresses(auto_scale_group_resource_id):
    """
        Get public ip addresses for all ec2 instances in a given auto scale group
        :param auto_scale_group_resource_id: string
        :return: list of public ip address
    """

    group = get_auto_scaling_group(auto_scale_group_resource_id)
    public_ip_addresses = []

    if group:
        for asg_instance in group.get('Instances'):
            instance_id = asg_instance.get('InstanceId')
            ip_address = get_public_ip_address(instance_id)

            public_ip_addresses.append(ip_address)

    return public_ip_addresses


def get_auto_scaling_group(resource_id):
    """
        Get autoscale group by resource_id
        :param resource_id:
        :return: boto autoscale group object
    """

    if not resource_id:
        return None

    client = boto3.client('autoscaling')
    names = [resource_id]
    groups = client.describe_auto_scaling_groups(AutoScalingGroupNames=names)

    if groups:
        return groups.get('AutoScalingGroups')[0]

    return None


def get_public_ip_address(ec2_instance_id):
    """
        Get EC2 instance public ip address
        :param ec2_instance_id:
        :return: string, public ip address
    """

    ec2 = boto3.resource('ec2')
    ec2_instance = ec2.Instance(ec2_instance_id)
    public_ip = ec2_instance.public_ip_address

    print(public_ip)

    return public_ip


def create_new_ecs_task_instances(cluster_name, task_definition, number_of_tasks):
    """
        Create new ECS cluster tasks instances
        :param cluster_name: ecs cluster name to spin up instances in
        :param task_definition: task definition to use for the instances
        :param number_of_tasks: number of tasks to spin up (will fail if there aren't enough
                                resources in the corresponding auto scaling group.
        :return: True if successful, False otherwise
    """

    if not cluster_name and not task_definition and number_of_tasks <= 0:
        return False

    ecs_client = boto3.client('ecs')
    response = ecs_client.run_task(cluster=cluster_name, taskDefinition=task_definition, count=number_of_tasks)

    if response:
        failures = response.get('failures')

        if len(failures) <= 0:
            return True
        else:
            return False

    return False
