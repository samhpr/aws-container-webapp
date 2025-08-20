"""
Mock AWS services for demo mode.
These mocks return realistic sample data without making actual AWS API calls.
"""

import json
import random
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any


class MockCloudWatch:
    """Mock CloudWatch client that returns realistic demo data"""
    
    def get_metric_statistics(self, namespace: str, metric_name: str, dimensions: List[Dict], 
                            start_time: datetime, end_time: datetime, period: int, statistics: List[str]) -> List[Dict]:
        """Generate mock CPU utilization data"""
        
        # Generate realistic timestamps
        current_time = start_time
        datapoints = []
        
        # Different baseline CPU percentages based on service type
        if namespace == 'AWS/ECS' and any(d.get('Value', '').endswith('fargate-service') for d in dimensions):
            base_cpu = 0.001635  # Very low for Fargate
        elif namespace == 'AWS/ECS' and any(d.get('Value', '').endswith('ec2-service') for d in dimensions):
            base_cpu = 0.000851  # Low for ECS on EC2
        elif namespace == 'AWS/EC2':
            instance_id = next((d['Value'] for d in dimensions if d['Name'] == 'InstanceId'), '')
            if 'EXAMPLE003' in instance_id or 'EXAMPLE004' in instance_id:  # EKS instances
                base_cpu = 2.84  # Higher for EKS
            else:  # Plain EC2 instances
                base_cpu = 0.472  # Medium for plain EC2
        elif namespace == 'AWS/AutoScaling':
            base_cpu = 0.472  # Same as plain EC2
        else:
            base_cpu = 0.1  # Default
        
        while current_time < end_time:
            # Add some realistic variation
            variation = random.uniform(-0.2, 0.2) * base_cpu
            cpu_value = max(0, base_cpu + variation)
            
            datapoints.append({
                'timestamp': current_time.isoformat(),
                'value': cpu_value
            })
            
            current_time += timedelta(seconds=period)
        
        return datapoints


class MockECS:
    """Mock ECS client for demo purposes"""
    
    def describe_services(self, cluster: str, services: List[str]) -> Dict[str, Any]:
        """Return mock service status"""
        mock_services = []
        
        for service_name in services:
            # Most services are active in demo mode
            running_count = 1 if random.random() > 0.1 else 0
            desired_count = 1
            
            mock_services.append({
                'serviceName': service_name,
                'clusterArn': f'arn:aws:ecs:us-west-2:123456789012:cluster/{cluster}',
                'serviceArn': f'arn:aws:ecs:us-west-2:123456789012:service/{cluster}/{service_name}',
                'taskDefinition': f'arn:aws:ecs:us-west-2:123456789012:task-definition/example-app:1',
                'desiredCount': desired_count,
                'runningCount': running_count,
                'pendingCount': 0,
                'status': 'ACTIVE',
                'launchType': 'FARGATE' if 'fargate' in service_name else 'EC2'
            })
        
        return {'services': mock_services}


class MockEC2:
    """Mock EC2 client for demo purposes"""
    
    def describe_instances(self, InstanceIds: List[str]) -> Dict[str, Any]:
        """Return mock instance status"""
        reservations = []
        
        for instance_id in InstanceIds:
            # Most instances are running in demo mode
            state = 'running' if random.random() > 0.15 else 'stopped'
            
            instance = {
                'InstanceId': instance_id,
                'ImageId': 'ami-EXAMPLE123',
                'State': {
                    'Code': 16 if state == 'running' else 80,
                    'Name': state
                },
                'PrivateIpAddress': f'10.0.{random.randint(1, 254)}.{random.randint(1, 254)}',
                'VpcId': 'vpc-EXAMPLE',
                'SubnetId': 'subnet-EXAMPLE',
                'InstanceType': 't3.micro',
                'LaunchTime': (datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 24))).isoformat()
            }
            
            reservations.append({
                'ReservationId': f'r-{instance_id.replace("i-", "")}',
                'Instances': [instance]
            })
        
        return {'Reservations': reservations}


class MockSecretsManager:
    """Mock Secrets Manager for sensitive configuration"""
    
    def get_secret_value(self, SecretId: str) -> Dict[str, Any]:
        """Return mock secret values"""
        mock_secrets = {
            'example-db-credentials': {
                'SecretString': json.dumps({
                    'username': 'demo_user',
                    'password': 'demo_password',
                    'host': 'localhost',
                    'port': 5432,
                    'database': 'demo_db'
                })
            },
            'example-api-keys': {
                'SecretString': json.dumps({
                    'api_key': 'demo_api_key_12345',
                    'secret_key': 'demo_secret_key_67890'
                })
            }
        }
        
        return mock_secrets.get(SecretId, {'SecretString': '{"demo": "value"}'})


class MockS3:
    """Mock S3 client for file operations"""
    
    def __init__(self):
        self.mock_objects = {
            'example-bucket-1234': [
                'demo-data/metrics.json',
                'demo-data/config.json',
                'demo-data/sample-file.txt'
            ]
        }
    
    def list_objects_v2(self, Bucket: str, Prefix: str = '') -> Dict[str, Any]:
        """Return mock S3 object listing"""
        objects = []
        
        if Bucket in self.mock_objects:
            for key in self.mock_objects[Bucket]:
                if key.startswith(Prefix):
                    objects.append({
                        'Key': key,
                        'LastModified': datetime.now(timezone.utc) - timedelta(days=random.randint(1, 30)),
                        'Size': random.randint(1024, 1024000),
                        'StorageClass': 'STANDARD'
                    })
        
        return {
            'Contents': objects,
            'IsTruncated': False,
            'KeyCount': len(objects)
        }
    
    def get_object(self, Bucket: str, Key: str) -> Dict[str, Any]:
        """Return mock S3 object content"""
        mock_content = {
            'demo-data/metrics.json': json.dumps({
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'metrics': {'cpu': 1.5, 'memory': 45.2, 'disk': 23.1}
            }),
            'demo-data/config.json': json.dumps({
                'app_name': 'Demo App',
                'version': '1.0.0',
                'environment': 'demo'
            })
        }
        
        content = mock_content.get(Key, '{"demo": "content"}')
        
        return {
            'Body': type('MockStreamingBody', (), {'read': lambda: content.encode()})(),
            'ContentLength': len(content),
            'ContentType': 'application/json' if Key.endswith('.json') else 'text/plain'
        }
