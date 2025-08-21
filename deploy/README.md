# 🚀 AWS Deployment Templates

**Production-ready Infrastructure as Code (IaC) templates** for deploying containerized applications across multiple AWS platforms.

> 💡 **New to this repo?** Check out our [**Deployment Decision Guide**](./DEPLOYMENT_GUIDE.md) for quick platform selection and recruiter-friendly explanations.

## 🎯 What This Demonstrates

- **Multi-platform AWS expertise**: ECS Fargate, ECS EC2, EKS/Kubernetes
- **Production-ready configurations**: Security, scaling, monitoring, load balancing  
- **DevOps best practices**: Infrastructure as Code, containerization, CI/CD ready
- **Enterprise patterns**: IRSA, ALB integration, auto-scaling, health checks

## 📁 Repository Structure

```
deploy/
├── 📄 DEPLOYMENT_GUIDE.md          # 🎯 START HERE - Platform selection guide
├── 📄 README.md                    # Technical documentation  
└── templates/
    ├── 🐳 ecs-fargate-task-definition.json    # Serverless container deployment
    ├── 🐳 ecs-ec2-task-definition.json        # Cost-optimized container deployment  
    └── ⚙️ k8s/                                # Complete Kubernetes ecosystem
        ├── example-app-deployment.yaml        # Core app: deployment + service + IRSA
        ├── example-app-ingress.yaml           # Application ingress (ALB)
        ├── nginx-deployment.yaml              # NGINX reverse proxy
        ├── nginx-ingress-alb.yaml             # NGINX ingress configuration
        ├── hpa.yaml                          # Horizontal Pod Autoscaler
        ├── iam_policy.json                   # AWS Load Balancer Controller IAM
        ├── v2_7_2_full.yaml                  # Complete ALB Controller installation
        └── containerd-upgrade-userdata.sh     # EKS node runtime upgrade
```

## 🏗️ Deployment Options

| Platform | Use Case | Complexity | Files Needed |
|----------|----------|------------|--------------|
| **ECS Fargate** | Quick demos, serverless | ⭐⭐ | `ecs-fargate-task-definition.json` |
| **ECS EC2** | Production, cost optimization | ⭐⭐⭐ | `ecs-ec2-task-definition.json` |
| **Basic K8s** | Learning, simple apps | ⭐⭐⭐ | `k8s/example-app-*` |
| **Production K8s** | Enterprise, full features | ⭐⭐⭐⭐⭐ | Complete `k8s/` directory |

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

1. **Update Configuration Values**
   ```bash
   # Replace placeholder values in all k8s manifests
   cd k8s/
   sed -i 's/123456789012/YOUR_ACCOUNT_ID/g' *.yaml
   sed -i 's/us-west-2/YOUR_REGION/g' *.yaml
   sed -i 's/example-eks-cluster/YOUR_CLUSTER_NAME/g' *.yaml
   ```

2. **Deploy Core Application**
   ```bash
   # Deploy main application components
   kubectl apply -f k8s/example-app-deployment.yaml
   kubectl apply -f k8s/example-app-ingress.yaml
   ```

3. **Deploy Supporting Components (Optional)**
   ```bash
   # Deploy NGINX and autoscaling
   kubectl apply -f k8s/nginx-deployment.yaml
   kubectl apply -f k8s/nginx-ingress-alb.yaml
   kubectl apply -f k8s/hpa.yaml
   ```

4. **Install AWS Load Balancer Controller (If needed)**
   ```bash
   # Apply IAM policy first, then install controller
   kubectl apply -f k8s/v2_7_2_full.yaml
   ```

## Configuration Variables

These templates use placeholder values that must be replaced:

- `123456789012` → Your AWS Account ID
- `us-west-2` → Your AWS Region
- `example-*` → Your specific resource names
- `EXAMPLE*` → Your specific instance/resource IDs
- `example-eks-cluster` → Your EKS cluster name

## Kubernetes Deployment Architecture

The `k8s/` directory contains a comprehensive set of manifests for production-ready Kubernetes deployment:

### Core Application Components
- **Application Deployment**: Includes deployment, service, and service account with IRSA configuration
- **Ingress**: Configured for AWS Load Balancer Controller with ALB integration
- **Autoscaling**: HPA configuration for automatic pod scaling based on CPU metrics

### Supporting Infrastructure  
- **NGINX**: Optional NGINX deployment for reverse proxy or static content serving
- **Load Balancer Controller**: Complete AWS Load Balancer Controller installation with CRDs
- **IAM Policies**: Required policies for AWS Load Balancer Controller functionality

### Node Configuration
- **Container Runtime**: Script for upgrading containerd to version 2.0.5 on EKS nodes

## 💼 For Recruiters & Hiring Managers

This deployment directory showcases:

- **AWS Proficiency**: Deep understanding of ECS, EKS, ALB, IAM, ECR
- **Kubernetes Expertise**: Production-grade manifests, not toy examples
- **DevOps Maturity**: Proper separation of concerns, security best practices
- **Real-World Experience**: Handles complexities like IRSA, load balancer controllers, autoscaling

**Quick Demo Path**: Use `DEPLOYMENT_GUIDE.md` for a 5-minute walkthrough of capabilities.

## 🔒 Security Considerations

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
