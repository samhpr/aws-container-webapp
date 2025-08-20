# AWS Container Platform Comparison

A comprehensive analysis and implementation of containerized applications across multiple AWS platforms, comparing cost, performance, setup complexity, and operational overhead.

## Project Overview

This project designs, implements, and analyzes a highly available, auto-scaling containerized web application on AWS. The baseline solution uses Amazon ECS with EC2, Application Load Balancer, AWS WAF, and CPU-based auto-scaling.

The analysis extends into a comparative study of four AWS container platforms—ECS-EC2, ECS-Fargate, plain EC2 with Docker, and EKS—using real AWS CloudWatch monitoring data and cost allocation tags to evaluate each platform's strengths and trade-offs.

## Demo Application

![Intro Animation](.github/media/introgif.gif)

The demo application is a Flask-based web dashboard that visualizes real-time container performance metrics and cost analysis. It demonstrates practical containerization patterns while showcasing the comparative analysis results.

![Interactive Charts](.github/media/interactivecharts.gif)

![Cost Analysis](.github/media/CostSection.gif)

📹 **[Full Application Demo Video](.github/media/FullAppRecord.mp4)**

## Key Findings

### Cost Analysis
- **ECS-Fargate**: $0.61 - Most cost-effective with minimal setup and zero infrastructure overhead
- **ECS-EC2**: $1.08 - Balanced cost with more infrastructure control (baseline)
- **Plain EC2**: $1.08 - Same cost as ECS-EC2 but requires full manual management
- **EKS**: $10.33 - Most expensive (9.6x baseline) due to Kubernetes control plane and overhead

![Decision Tree](.github/media/DecisionTree.gif)

### Performance Insights
- **ECS-Fargate**: 0.001635% average CPU utilization - extremely efficient resource usage
- **ECS-EC2**: 0.000851% average CPU utilization - good container orchestration efficiency
- **Plain EC2**: 0.472% average CPU utilization - 555x higher than ECS due to OS overhead
- **EKS**: 2.84% average CPU utilization - 3340x higher due to Kubernetes system overhead

### Setup Complexity
- **ECS-Fargate**: 30-45 minutes, minimal troubleshooting
- **ECS-EC2**: 45-60 minutes + 2 hours troubleshooting (memory limits, security groups)
- **Plain EC2**: 30-40 minutes, straightforward but manual configuration
- **EKS**: 4+ hours including containerd version issues and load balancer controller setup

## Architecture

The application implements a microservices architecture demonstrating real-world containerization patterns:

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │
│   (Nginx)       │◄──►│   (Flask)       │
│   Port 3000     │    │   Port 8000     │
└─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │   AWS Services  │
                       │   (Production)  │
                       │   Mock Services │
                       │   (Demo Mode)   │
                       └─────────────────┘
```

### Backend Implementation
- **Flask REST API** with CloudWatch metrics integration
- **Service abstraction layer** supporting both production AWS services and demo mock services
- **Real-time metrics collection** from ECS, EC2, and EKS platforms
- **Health monitoring** with comprehensive service status checking
- **Security headers** and proper error handling

### Frontend Implementation
- **Interactive dashboard** with Chart.js visualizations
- **Responsive design** with Apple-style animations and transitions
- **Real-time data updates** from backend API endpoints
- **Decision tree tool** for platform selection guidance
- **Cost comparison tools** with detailed breakdowns

### Mock Services (Demo Mode)
- **Realistic data generation** matching actual AWS CloudWatch patterns
- **Service simulation** for ECS, EC2, EKS, and supporting AWS services
- **No external dependencies** - runs completely offline
- **Authentic metrics** reflecting real platform performance characteristics

## Technical Implementation

### Container Orchestration Patterns
- **Multi-stage Docker builds** with security best practices
- **Health checks** and graceful shutdown handling
- **Service discovery** and inter-container communication
- **Environment-based configuration** management

### Infrastructure as Code
Ready-to-deploy templates included:
- **ECS Task Definitions** for both Fargate and EC2 launch types
- **Kubernetes manifests** with proper resource management
- **Security configurations** with IAM roles and policies
- **Auto-scaling policies** based on CPU utilization

### Monitoring and Observability
- **CloudWatch integration** for metrics collection
- **Application Performance Monitoring** with request logging
- **Resource utilization tracking** across all platforms
- **Cost allocation tagging** for accurate financial analysis

## Challenges Overcome

1. **ECS-EC2 Memory Management**: Resolved memory allocation conflicts between task definitions and EC2 instance resources
2. **Application Load Balancer Security**: Configured ephemeral port ranges for dynamic port mapping
3. **EKS Complexity**: Managed containerd version compatibility and AWS Load Balancer Controller installation
4. **Cost Attribution**: Implemented comprehensive tagging strategy for accurate cross-platform cost comparison

## Quick Start (Demo Mode)

```bash
# Clone and setup
git clone https://github.com/samhpr/aws-container-webapp.git
cd aws-container-webapp

# Start the demo application
cp .env.example .env
docker-compose up --build
```

Access the application:
- **Main Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/health
- **Metrics Endpoint**: http://localhost:8000/api/metrics

## Production Deployment

The repository includes production-ready deployment templates:

- **ECS Fargate**: Serverless containers with automatic scaling
- **ECS on EC2**: Container orchestration with infrastructure control
- **Kubernetes (EKS)**: Full Kubernetes deployment with auto-scaling
- **Plain EC2**: Traditional Docker deployment

See `deploy/README.md` for detailed deployment instructions.

## Conclusions

### Platform Recommendations

**For lightweight workloads and rapid development:**
- **ECS Fargate** - Optimal cost-efficiency and operational simplicity

**For consistent workloads requiring infrastructure control:**
- **ECS on EC2** - Better cost-effectiveness at higher utilization (>55%)

**For learning infrastructure management:**
- **Plain EC2 with Docker** - Maximum control and understanding

**For enterprise-scale applications requiring advanced orchestration:**
- **EKS** - Justified only when Kubernetes-specific features are essential

### Cost-Performance Breakpoints
- **Fargate advantage**: Below 55% sustained utilization
- **EC2 advantage**: Above 55% sustained utilization
- **EKS justification**: Only with advanced K8s feature requirements

## Future Enhancements

- **Load testing analysis**: Synthetic testing at 25%, 50%, 75% CPU utilization
- **Multi-AZ deployment patterns**: High availability configurations
- **Advanced auto-scaling**: Custom CloudWatch metrics and predictive scaling
- **Security hardening**: Container image scanning and runtime protection

## Tech Stack

- **Backend**: Flask (Python), AWS SDK (boto3), CloudWatch integration
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js for visualizations
- **Infrastructure**: Docker, Docker Compose, AWS ECS/EKS/EC2
- **Monitoring**: CloudWatch metrics, Application Performance Monitoring
- **Deployment**: Infrastructure as Code templates for multiple platforms

---

*This project demonstrates practical experience with AWS container services, infrastructure automation, and performance optimization in cloud environments.*