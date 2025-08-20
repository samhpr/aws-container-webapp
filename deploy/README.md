# Deployment Templates

This directory contains generic Infrastructure as Code (IaC) templates for deploying the containerized application to various AWS platforms.

## Available Templates

### ECS Templates
- `ecs-fargate-task-definition.json` - Task definition for ECS Fargate deployment
- `ecs-ec2-task-definition.json` - Task definition for ECS on EC2 deployment

### Kubernetes Templates
- `k8s-deployment.yaml` - Kubernetes deployment, service, and service account

## Prerequisites

Before using these templates, ensure you have:

1. **AWS Account Setup**
   - AWS CLI configured with appropriate credentials
   - Required IAM roles and policies created
   - ECR repository for container images

2. **Container Registry**
   - Application image built and pushed to ECR
   - Image URI updated in template files

3. **Network Configuration**
   - VPC with appropriate subnets configured
   - Security groups allowing necessary traffic
   - Load balancer configuration (for production)

## Usage Instructions

### For ECS Deployment

1. **Update Image URI**
   ```bash
   # Replace placeholder values in task definition
   sed -i 's/123456789012/YOUR_ACCOUNT_ID/g' ecs-fargate-task-definition.json
   sed -i 's/us-west-2/YOUR_REGION/g' ecs-fargate-task-definition.json
   ```

2. **Create Task Definition**
   ```bash
   aws ecs register-task-definition --cli-input-json file://ecs-fargate-task-definition.json
   ```

3. **Create/Update Service**
   ```bash
   aws ecs create-service \
     --cluster example-fargate-cluster \
     --service-name example-app-fargate-service \
     --task-definition example-app-fargate:1 \
     --desired-count 2
   ```

### For Kubernetes Deployment

1. **Update Image URI**
   ```bash
   # Replace placeholder values
   sed -i 's/123456789012/YOUR_ACCOUNT_ID/g' k8s-deployment.yaml
   sed -i 's/us-west-2/YOUR_REGION/g' k8s-deployment.yaml
   ```

2. **Deploy to Cluster**
   ```bash
   kubectl apply -f k8s-deployment.yaml
   ```

## Configuration Variables

These templates use placeholder values that must be replaced:

- `123456789012` → Your AWS Account ID
- `us-west-2` → Your AWS Region
- `example-*` → Your specific resource names
- `EXAMPLE*` → Your specific instance/resource IDs

## Security Considerations

- **IAM Roles**: Ensure minimal required permissions
- **Network Security**: Configure security groups appropriately
- **Secrets Management**: Use AWS Secrets Manager or Parameter Store for sensitive data
- **Image Security**: Scan container images for vulnerabilities

## Monitoring and Logging

- **CloudWatch Logs**: Configured in task definitions
- **Health Checks**: HTTP health check endpoints configured
- **Metrics**: CloudWatch container insights available

## Cost Optimization

- **Resource Sizing**: Adjust CPU/memory based on actual usage
- **Auto Scaling**: Configure based on metrics and demand
- **Spot Instances**: Consider for non-critical workloads (EC2 deployments)

## Troubleshooting

Common issues and solutions:

1. **Image Pull Errors**: Verify ECR permissions and image URI
2. **Service Discovery**: Check VPC configuration and security groups
3. **Health Check Failures**: Verify application startup time and endpoint
4. **Resource Limits**: Monitor CloudWatch metrics for resource utilization

For more detailed AWS-specific guidance, refer to the official AWS documentation for each service.
