from flask import Flask
import boto3
import time
from botocore.exceptions import ClientError
from flask import request

app = Flask(__name__)

def stop_instance(instance_id):

    # Terminate each instance in the argument list
    ec2 = boto3.client('ec2')

    states = None
    try:
        states = ec2.stop_instances(InstanceIds=[instance_id])
    except ClientError as e:
        print(e)
    return states

def start_instance(instance_id):

    # Terminate each instance in the argument list
    ec2 = boto3.client('ec2')

    try:
        states = ec2.start_instances(InstanceIds=[instance_id])
    except ClientError as e:
        print(e)
    return states

@app.route('/')
def index():

    return "Hello World!"

@app.route('/restart')
def instance_restart():

    instance_id = request.args.get('id')

    force_update = request.args.get('force')

    print(force_update)

    states = None

    if (force_update == "true") and (instance_id is not None):

        states = stop_instance(instance_id)

        if states is not None:
            print('Stopping the EC2 instance')
            #for state in states:
            #    print(state['ResponseMetadata'])

        time.sleep(60)

        states = start_instance(instance_id)

        if states is not None:
            print('Starting the EC2 instance')
            #for state in states:
            #    print(state['ResponseMetadata'])

            return "Done"

        else:

            return "Error"

    else:

        return "Value not passed"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)