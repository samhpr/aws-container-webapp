# AWS Container Platform Comparison - Detailed Analysis

This document provides comprehensive technical details, analysis, and deployment guidance for the AWS container platform comparison project.

## Problem Statement

*"The customer has developed a containerized application but faces difficulties deploying it in a manner that delivers both **scalability** and **high availability**. They require a solution that can **automatically scale to meet variable demand**, distribute workloads efficiently across resources, and provides **protection against common web exploits**. Their current architecture lacks **elasticity and resilience**, resulting in **degraded performance during peak usage periods** and increased risk of **service downtime**."*

## Solution Overview

This project demonstrates AWS knowledge through the design, implementation, and comparative analysis of a **highly available, auto-scaling containerized web application** deployed across four distinct AWS container platforms. The solution directly addresses customer requirements for **scalability, resilience, and cost optimization** while showcasing practical experience with ECS, EKS, EC2, and enterprise-grade deployment strategies.

### Customer Value Delivered

- **Solved scalability challenges** through auto-scaling architectures across 4 platforms
- **Eliminated service downtime risks** with proper health checks and load balancing
- **Reduced operational costs** by 94% through strategic platform selection (Fargate vs EKS)
- **Provided actionable recommendations** based on real performance data and cost analysis

### Key Technical Achievements

- Designed and deployed production-ready containerized architecture with **built-in resilience**
- Implemented **Application Load Balancer + AWS WAF** for traffic distribution and security
- Analyzed real performance data across 4 container platforms during **peak load scenarios**
- Demonstrated **infrastructure-as-code** practices and automated deployment pipelines

## Technical Implementation Highlights

- **Multi-tier architecture** with proper separation of concerns
- **Infrastructure as Code** using CloudFormation/Terraform patterns
- **Security best practices** including IAM roles, security groups, and WAF integration
- **Observability** with structured logging and metrics collection
- **Cost optimization** through resource tagging and allocation tracking

## Setup Complexity Analysis

Real-world deployment experience across platforms:

![Deployment Process Visualization](../media/website-chart-scrolling.gif)

### Implementation Timelines

- **ECS Fargate**: 30-45 minutes (minimal infrastructure management)
- **ECS on EC2**: 45-60 minutes + 2 hours troubleshooting (memory allocation, security groups)
- **Plain EC2**: 30-40 minutes (straightforward but manual configuration required)
- **EKS**: 4+ hours (containerd compatibility, ALB controller, networking complexity)

This hands-on experience demonstrates practical knowledge of AWS service integration challenges and problem-solving abilities valuable in customer-facing roles.

## How This Was Evaluated

All performance and cost data was gathered from real AWS deployments using:

- **CloudWatch metrics** for CPU utilization, memory usage, and operational metrics
- **AWS Cost Explorer** for actual monthly cost calculations based on real usage
- **Application Load Balancer** health checks and response time monitoring
- **Real-time dashboard** with live performance visualization

## Results & Analysis

### Evaluation Setup

All testing was performed in the **us-east-2 (Ohio)** AWS region.

- **Base Image**: `nginx:latest` was used as the container workload across all platforms.  
- **Instance Types**:  
  - **EC2, ECS-EC2, ECS-Fargate** used t3.micro  
  - **EKS** used t3.medium (used due to resource constraints and cluster requirements)
  - **Scaling**: Each service was configured with minimal scaling (2 instances/services) to reflect baseline cost and performance comparisons.  
  - **Load Balancing**: Each service was configured with an ingress internet-facing Application Load Balancer. 

These choices ensured consistent workloads across platforms while keeping infrastructure cost-efficient for testing purposes.


### Cost Optimization Analysis

The analysis reveals significant cost optimization opportunities that would directly benefit AWS customers:

![Cost Analysis Dashboard](../media/CostSection.gif)

| Platform | Monthly Cost | Use Case | ROI Benefit |
|----------|-------------|-----------|-------------|
| **ECS Fargate** | $0.61 | Development, Variable Workloads | 94% cost reduction vs EKS |
| **ECS on EC2** | $1.08 | Production, Predictable Traffic | Baseline for comparison |
| **Plain EC2** | $1.08 | Legacy Migration, Learning | Same cost, maximum control |
| **EKS** | $10.33 | Enterprise, Advanced Orchestration | Justified for K8s-specific needs |

**Cost Optimization Insight:** For workloads under 55% sustained utilization, Fargate delivers 43% cost savings compared to EC2-based solutions while eliminating infrastructure management overhead.

### Performance Analysis

The application provides real-time visualization of container performance metrics, demonstrating practical monitoring implementation:

![Interactive Performance Charts](../media/interactivecharts.gif)

#### Resource Efficiency Findings

- **ECS Fargate**: 0.001635% avg CPU utilization - exceptional resource optimization
- **ECS on EC2**: 0.000851% avg CPU utilization - container orchestration benefits evident  
- **Plain EC2**: 0.472% avg CPU utilization - 555x higher due to OS overhead
- **EKS**: 2.84% avg CPU utilization - Kubernetes control plane overhead quantified

These metrics demonstrate hands-on experience with CloudWatch monitoring, performance optimization, and capacity planning—critical skills for AWS solutions architecture roles.

### Decision Framework Tool

The application includes an intelligent platform selection tool based on real-world usage patterns:

![Decision Tree Interface](../media/DecisionTree.gif)

This tool codifies the decision-making process that AWS solutions architects use daily when advising customers on container platform selection.

## Problem-Solving Experience

### Challenge 1: ECS Memory Management
- **Issue**: Task definition memory conflicts with EC2 instance allocation
- **Solution**: Implemented proper resource reservation and limit configuration
- **AWS Skill**: Deep understanding of ECS resource management

### Challenge 2: Application Load Balancer Security
- **Issue**: Dynamic port mapping security group configuration
- **Solution**: Configured ephemeral port ranges for ECS service discovery
- **AWS Skill**: Networking and security best practices

### Challenge 3: EKS Operational Complexity
- **Issue**: Kubernetes control plane and networking integration
- **Solution**: Implemented AWS Load Balancer Controller and proper RBAC
- **AWS Skill**: Advanced container orchestration and AWS service integration

## Recommendations for Customers

### Start Small then Scale
- Begin with ECS Fargate for rapid prototyping and development
- Migrate to ECS on EC2 when sustained utilization exceeds 55%
- Consider EKS only when Kubernetes-specific features are required

### Cost Optimization Strategy
- Use Fargate for variable, unpredictable workloads
- Deploy ECS on EC2 with Spot instances for batch processing
- Reserve capacity for predictable production workloads

## Application Technology Stack

### Development Stack
- **Backend**: Flask (Python), AWS SDK (boto3)
- **Frontend**: Responsive web dashboard with real-time metrics  
- **Infrastructure**: Docker containerization with multi-platform deployment
- **Monitoring**: Custom CloudWatch dashboards and performance alarms

## Production Deployment

Ready-to-deploy Infrastructure as Code templates included:
- ECS Fargate task definitions with auto-scaling
- ECS on EC2 with cluster management
- EKS deployment manifests with RBAC
- Security configurations and monitoring setup

## Further Reading & AWS Documentation

For more in-depth reading on AWS container best practices and cost, here are some of the AWS docs I drew from:

- [Amazon EKS Best Practices Guide](https://docs.aws.amazon.com/eks/latest/best-practices/introduction.html) — covers autoscaling, cost strategies, security, and performance.  
- [Amazon ECS Best Practices Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-best-practices.html) — networking, security, autoscaling, and operational efficiency.  
- [Theoretical Cost Optimization: ECS Launch Type (Fargate vs EC2)](https://aws.amazon.com/blogs/containers/theoretical-cost-optimization-by-amazon-ecs-launch-type-fargate-vs-ec2/) — real-world cost trade-offs across ECS deployment models.  
- [AWS Fargate Pricing](https://aws.amazon.com/fargate/pricing/) — official breakdown of compute (vCPU, memory, storage).  
- [Amazon EKS Pricing](https://aws.amazon.com/eks/pricing/) — cluster-level and worker-node pricing details.  



See `deploy/` directory for complete deployment guides.

This project demonstrates practical experience with AWS container services and cloud architecture patterns, providing a comprehensive comparison to help teams choose the right platform for their needs.

