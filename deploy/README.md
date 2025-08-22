# How to deploy on AWS

These manifests/templates are sanitized. Replace placeholders before use:
- `123456789012` -> your AWS account ID
- `us-west-2` -> your AWS region
- `example-*`, `EXAMPLE*` -> your resource names/IDs
- Image URI -> your ECR image URI

## ECS Fargate (quick demo)
1) Update placeholders in `deploy/ecs-fargate-task-definition.json`.
2) Register the task definition:
```bash
aws ecs register-task-definition \
  --cli-input-json file://deploy/ecs-fargate-task-definition.json
```
3) Create or update your ECS service as needed (cluster, service name, desired count).

## ECS on EC2
1) Update placeholders in `deploy/ecs-ec2-task-definition.json`.
2) Register the task definition:
```bash
aws ecs register-task-definition \
  --cli-input-json file://deploy/ecs-ec2-task-definition.json
```
3) Create or update your ECS service as needed.

## Kubernetes (EKS or any cluster with ALB controller)
1) Update placeholders in the manifests, then apply:
```bash
kubectl apply -f deploy/k8s/app-deployment.yaml
kubectl apply -f deploy/k8s/app-service.yaml
kubectl apply -f deploy/k8s/app-ingress.yaml
# Optional autoscaling:
kubectl apply -f deploy/k8s/hpa.yaml
```

### Prerequisites
- [AWS CLI](https://aws.amazon.com/cli/) configured with appropriate permissions
- [kubectl](https://kubernetes.io/docs/tasks/tools/) for cluster management
- [eksctl](https://eksctl.io/) for EKS cluster creation 


## AWS Documentation

Heres the AWS documentation I used to help deploy my systems:

**EKS / Ingress & Load Balancer**
- [EKS Load Balancer & Controller](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html)
- [AWS Load Balancer Controller GitHub (manifests/helm)](https://github.com/kubernetes-sigs/aws-load-balancer-controller)

**EKS / CLI Tools**
- [eksctl (official site)](https://eksctl.io/)
- [Install eksctl (AWS Docs)](https://docs.aws.amazon.com/eks/latest/eksctl/installation.html)
- [Install kubectl (AWS Docs)](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html)
- [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html)

**Performance & Cost Monitoring**
- [Cost Allocation Tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html)
- [Container Insights (EKS & ECS)](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContainerInsights.html)
- [EKS CloudWatch Observability Add-on](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/installCloudWatch-Observability-EKS-addon.html)
- [EKS CloudWatch Application Signals](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Application-Signals-EnableEKS.html)
- [AWS WAF Logging](https://docs.aws.amazon.com/waf/latest/developerguide/logging.html)
- [AWS WAF Rules Reference](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rules.htm)

**ECS, Fargate, EC2**
- [Amazon ECS Developer Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html)
- [ECS Task Definitions & Memory](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)
- [ECS Service Auto Scaling](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-autoscaling.html)
- [EC2 User Data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)

**Base Workload**
- [Nginx Overview](https://en.wikipedia.org/wiki/Nginx)
- [Nginx Officia]()

### Notes:
- Make sure your cluster has the AWS Load Balancer Controller installed if using ALB ingress.
- Make sure the image URI and namespaces match your environment.
