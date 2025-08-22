# Deploy

These manifests/templates are sanitized. Replace placeholders before use:
- `123456789012` → your AWS account ID
- `us-west-2` → your AWS region
- `example-*`, `EXAMPLE*` → your resource names/IDs
- Image URI → your ECR image URI

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

### Notes:
- Ensure your cluster has the AWS Load Balancer Controller installed if using ALB ingress.
- Ensure the image URI and namespaces match your environment.
