import boto3

# Remove instances that are not tagged with an owner or name in the specified VPC

def handler(event, context):
    ec2_conn = boto3.resource('ec2')
    instances = ec2_conn.instances.filter(Filters=[{'Name': 'vpc-id', 'Values': ['YOUR_VPC_ID']}, ])

    terminated_instances = list()
    for instance in instances:
        if instance.tags:
            if not any(d['Key'] == 'Name' for d in instance.tags) and not any(d['Key'] == 'OWNER' for d in instance.tags):
                instance.terminate()
                terminated_instances.append(instance)
        if not instance.tags:
            instance.terminate()
            terminated_instances.append(instance)

    print "terminated {0} instances".format(len(terminated_instances))
    for terminated in terminated_instances:
        print (terminated.id, terminated.instance_type)
