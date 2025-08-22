# AWS Container Platform Comparison

AWS-based web application comparing container deployment options (ECS Fargate, ECS on EC2, EC2, EKS) with focus on performance and cost trade-offs.

![Application Demo](media/introgif.gif)

## Quick Start

Experience the interactive dashboard locally:

```bash
git clone https://github.com/samhpr/aws-container-webapp.git
cd aws-container-webapp
cp .env.example .env
docker-compose up --build
```

Access at: http://localhost:3000

## Results at a Glance

• **Cost**: 94% lower monthly cost with Fargate ($0.61) vs EKS ($10.33) for demo workload  
• **Performance**: CPU utilization ranges from 0.001% (Fargate) to 2.84% (EKS) - 555x efficiency variance  
• **Complexity**: Fargate easiest (30-45 min); EKS most flexible and complex (4+ hours)  
• **Security**: IAM roles, VPC/security groups, ALB + WAF patterns applied across all platforms  
• **Monitoring**: CloudWatch metrics, logs, and real-time performance dashboards integrated  
• **Decision Tool**: Interactive platform selector based on workload characteristics and requirements  

## AWS Services & Skills

**Services:** ECS (Fargate/EC2), EKS, EC2 Auto Scaling, ALB, WAF, VPC/Security Groups/NACLs, IAM, CloudWatch, Secrets Manager, Systems Manager, Cost Explorer

**Skills:** Container orchestration, cost optimization, performance monitoring, security architecture, Infrastructure as Code patterns, customer decision frameworks

## Architectures

### ECS Fargate Architecture
![ECS Fargate Solution Architecture](media/diagrams/ECS-Fargate-SA-Diagram.png)
*Serverless container platform with minimal infrastructure management*

### ECS on EC2 Architecture  
![ECS on EC2 Solution Architecture](media/diagrams/ECS-EC2-SA-Diagram.png)
*Managed container orchestration with EC2 instance control*

### Plain EC2 with Docker Architecture
![EC2 Docker Solution Architecture](media/diagrams/EC2-Docker-SA-Diagram.png)
*Traditional virtualized approach with maximum flexibility*

### EKS Architecture
![EKS Solution Architecture](media/diagrams/EKS-SA-Diagram.png)
*Kubernetes-native platform for complex orchestration needs*

---

For challenges, deployment notes, and detailed analysis, see [docs/DETAILED.md](docs/DETAILED.md).