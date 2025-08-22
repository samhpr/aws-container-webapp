from flask import Flask, render_template, jsonify
import os
import json
import logging
from datetime import datetime, timedelta, timezone

# set up basic logging so we can see what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# figure out if we're using mock data or real aws
DEMO_MODE = os.environ.get('DEMO_MODE', 'true').lower() == 'true'

# add some basic security headers to all responses
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

# set up either mock services or real aws clients depending on demo mode
if DEMO_MODE:
    logger.info("Running in DEMO_MODE - using mock services")
    from mocks.aws_services import MockCloudWatch, MockECS, MockEC2
    cloudwatch = MockCloudWatch()
    ecs_client = MockECS()
    ec2_client = MockEC2()
else:
    logger.info("Running in production mode - using real AWS services")
    import boto3
    try:
        region = os.environ.get('AWS_REGION', 'us-west-2')
        cloudwatch = boto3.client('cloudwatch', region_name=region)
        ecs_client = boto3.client('ecs', region_name=region)
        ec2_client = boto3.client('ec2', region_name=region)
    except Exception as e:
        logger.error("Failed to initialize AWS clients: %s", str(e))
        cloudwatch = None
        ecs_client = None
        ec2_client = None

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/health')
def get_health():
    try:
        health_status = {}
        
        # see if our fargate service is running
        try:
            response = ecs_client.describe_services(
                cluster='example-fargate-cluster',
                services=['example-app-fargate-service']
            )
            if DEMO_MODE:
                service = response['services'][0]
            else:
                service = response['services'][0]
            health_status['ecs_fargate'] = 'active' if service['runningCount'] > 0 and service['desiredCount'] > 0 else 'inactive'
        except Exception:
            health_status['ecs_fargate'] = 'error'
        
        # check the ecs service running on ec2
        try:
            response = ecs_client.describe_services(
                cluster='example-ec2-cluster',
                services=['example-ecs-ec2-service']
            )
            if DEMO_MODE:
                service = response['services'][0]
            else:
                service = response['services'][0]
            health_status['ecs_ec2'] = 'active' if service['runningCount'] > 0 and service['desiredCount'] > 0 else 'inactive'
        except Exception:
            health_status['ecs_ec2'] = 'error'
        
        # see if our plain ec2 instances are up
        try:
            response = ec2_client.describe_instances(
                InstanceIds=['i-EXAMPLE001', 'i-EXAMPLE002']
            )
            running_count = 0
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    if instance['State']['Name'] == 'running':
                        running_count += 1
            health_status['plain_ec2'] = 'active' if running_count > 0 else 'inactive'
        except Exception:
            health_status['plain_ec2'] = 'error'
        
        # check if eks worker nodes are running
        try:
            response = ec2_client.describe_instances(
                InstanceIds=['i-EXAMPLE003', 'i-EXAMPLE004']
            )
            running_count = 0
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    if instance['State']['Name'] == 'running':
                        running_count += 1
            health_status['eks'] = 'active' if running_count > 0 else 'inactive'
        except Exception:
            health_status['eks'] = 'error'
        
        return jsonify(health_status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics')
def get_metrics():
    try:
        if cloudwatch is None:
            return jsonify({'error': 'CloudWatch client not available'}), 500
            
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=3)
        
        logger.info("Fetching metrics from %s to %s", start_time, end_time)
        
        metrics = {}
        
        # get cpu metrics for fargate service
        metrics['ecs_fargate'] = {
            'example-app-fargate-service': get_ecs_cpu('example-app-fargate-service', 'example-fargate-cluster', start_time, end_time)
        }
        
        # get cpu metrics for ecs on ec2
        metrics['ecs_ec2'] = {
            'example-ecs-ec2-service': get_ecs_cpu('example-ecs-ec2-service', 'example-ec2-cluster', start_time, end_time)
        }
        
        # grab cpu data from our plain ec2 boxes
        plain_ec2_instances = ['i-EXAMPLE001', 'i-EXAMPLE002']
        metrics['plain_ec2'] = {}
        for instance_id in plain_ec2_instances:
            metrics['plain_ec2'][instance_id] = get_single_ec2_cpu(instance_id, start_time, end_time)
        # also get the auto scaling group average
        metrics['plain_ec2']['example-ec2-asg'] = get_asg_cpu('example-ec2-asg', start_time, end_time)
        
        # get cpu from each eks worker node
        eks_instances = ['i-EXAMPLE003', 'i-EXAMPLE004']
        metrics['eks'] = {}
        for instance_id in eks_instances:
            metrics['eks'][instance_id] = get_single_ec2_cpu(instance_id, start_time, end_time)
        
        logger.info("All metrics fetched successfully")
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_ecs_cpu(service_name, cluster_name, start_time, end_time):
    try:
        if DEMO_MODE:
            return cloudwatch.get_metric_statistics(
                'AWS/ECS', 'CPUUtilization',
                [{'Name': 'ServiceName', 'Value': service_name},
                 {'Name': 'ClusterName', 'Value': cluster_name}],
                start_time, end_time, 300, ['Average']
            )
        else:
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/ECS',
                MetricName='CPUUtilization',
                Dimensions=[
                    {'Name': 'ServiceName', 'Value': service_name},
                    {'Name': 'ClusterName', 'Value': cluster_name}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average']
            )
            # sort the data points by time and keep all the decimal places
            sorted_points = sorted(response['Datapoints'], key=lambda x: x['Timestamp'])
            return [{'timestamp': point['Timestamp'].isoformat(), 'value': point['Average']} 
                    for point in sorted_points]
    except Exception:
        return []

def get_asg_cpu(asg_name, start_time, end_time):
    try:
        if DEMO_MODE:
            return cloudwatch.get_metric_statistics(
                'AWS/AutoScaling', 'GroupAverageCPUUtilization',
                [{'Name': 'AutoScalingGroupName', 'Value': asg_name}],
                start_time, end_time, 300, ['Average']
            )
        else:
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/AutoScaling',
                MetricName='GroupAverageCPUUtilization',
                Dimensions=[{'Name': 'AutoScalingGroupName', 'Value': asg_name}],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average']
            )
            # sort by time and keep the precision
            sorted_points = sorted(response['Datapoints'], key=lambda x: x['Timestamp'])
            return [{'timestamp': point['Timestamp'].isoformat(), 'value': point['Average']} 
                    for point in sorted_points]
    except Exception:
        return []

def get_single_ec2_cpu(instance_id, start_time, end_time):
    try:
        if DEMO_MODE:
            return cloudwatch.get_metric_statistics(
                'AWS/EC2', 'CPUUtilization',
                [{'Name': 'InstanceId', 'Value': instance_id}],
                start_time, end_time, 300, ['Average']
            )
        else:
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average']
            )
            # put data points in time order
            sorted_points = sorted(response['Datapoints'], key=lambda x: x['Timestamp'])
            return [{'timestamp': point['Timestamp'].isoformat(), 'value': point['Average']} 
                    for point in sorted_points]
    except Exception:
        return []

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('BACKEND_PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
