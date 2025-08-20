# Containerized Web App Demo

A comprehensive containerized web application demonstration showcasing different deployment platforms and their performance characteristics.

## Overview

This containerized web app (demo mode) demonstrates a React + Flask application with interactive monitoring dashboards that help you choose the right container platform for your needs. The application compares ECS Fargate, ECS on EC2, plain EC2 with Docker, and EKS across multiple dimensions including setup complexity, cost, and performance.

## Preview

![Intro Animation](.github/media/introgif.gif)

![Interactive Charts](.github/media/interactivecharts.gif)

![Cost Analysis](.github/media/CostSection.gif)

![Decision Tree](.github/media/DecisionTree.gif)

📹 **[Full Application Demo Video](.github/media/FullAppRecord.mp4)**

## What This Demonstrates

- **Containerized Architecture**: Flask backend + Nginx frontend with proper separation of concerns
- **Multiple Deployment Options**: Ready-to-deploy configurations for various container platforms
- **Interactive Monitoring**: Real-time metrics visualization and comparison dashboards
- **Cost Analysis**: Comprehensive cost breakdown and optimization recommendations  
- **Decision Support**: Interactive decision tree to guide platform selection
- **Mock Services**: Demonstrates service abstraction with switchable backend implementations
- **Production-Ready**: Health checks, logging, security headers, and proper error handling

## Tech Stack

- **Backend**: Flask (Python), Mock AWS services
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Infrastructure**: Docker, Docker Compose
- **Deployment**: ECS (Fargate/EC2), EKS, plain EC2
- **Monitoring**: CloudWatch metrics integration (mocked in demo)

## Local Quickstart

```bash
# Clone and setup
git clone <repository-url>
cd aws-container-webapp

# Start the application
cp .env.example .env
docker-compose up --build
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Main Dashboard**: http://localhost:3000 (proxied to backend)

## Demo Mode Notice

🎯 **This application runs in demo mode by default**, using mock data and services. No real AWS resources are accessed, making it safe to run anywhere without credentials.

- Mock CloudWatch metrics with realistic data patterns
- Simulated service health checks
- No external API calls or cloud dependencies
- All sensitive identifiers replaced with example placeholders

## Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │
│   (Nginx)       │◄──►│   (Flask)       │
│   Port 3000     │    │   Port 8000     │
└─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │   Mock Services │
                       │   (AWS Mocks)   │
                       └─────────────────┘
```

## Features

### 📊 Interactive Dashboards
- Real-time CPU utilization charts for all platforms
- Comparative analysis between deployment options
- Cost breakdown with visual pie charts
- Platform performance metrics

### 🎯 Decision Support Tool
- Interactive decision tree for platform selection
- Personalized recommendations based on requirements
- Experience level and priority-based guidance

### 💰 Cost Analysis
- Detailed cost breakdown per platform
- Monthly cost projections
- Resource utilization efficiency metrics

### 🔧 Production Deployment Templates
- ECS Fargate and EC2 task definitions
- Kubernetes deployment manifests
- Infrastructure as Code templates
- Security and monitoring configurations

## Project Structure

```
├── .github/media/          # Optimized demo media files
├── app/
│   ├── backend/           # Flask API server
│   ├── frontend/          # Static web frontend
│   └── mocks/            # Mock AWS services
├── deploy/
│   ├── templates/        # IaC templates (ECS, K8s)
│   └── README.md        # Deployment guide
├── docker-compose.yml    # Local development stack
├── .env.example         # Environment configuration template
└── README.md           # This file
```

## Development

### Running Individual Services

**Backend only:**
```bash
cd app/backend
pip install -r requirements.txt
DEMO_MODE=true python app.py
```

**Frontend only:**
```bash
cd app/frontend
# Serve with any static server
python -m http.server 3000
```

### Environment Variables

Key configuration options in `.env`:

- `DEMO_MODE=true` - Enable mock services (default)
- `FRONTEND_PORT=3000` - Frontend service port
- `BACKEND_PORT=8000` - Backend service port
- `AWS_REGION=us-west-2` - AWS region (for production mode)

## Production Deployment

Ready-to-use deployment templates are provided in `deploy/templates/`:

- **ECS Fargate**: Serverless containers with minimal management
- **ECS on EC2**: Container orchestration with server control  
- **Kubernetes**: Full K8s deployment with auto-scaling
- **Plain EC2**: Traditional server deployment with Docker

See `deploy/README.md` for detailed deployment instructions.

## Performance Insights

Based on the demo data, this application showcases:

- **ECS Fargate**: Lowest CPU overhead (0.001635%), best for variable workloads
- **ECS on EC2**: Balanced performance (0.000851%), good for consistent workloads  
- **Plain EC2**: Higher overhead (0.472%), maximum control and flexibility
- **EKS**: Highest overhead (2.84%), enterprise features and advanced orchestration

## Contributing

This is a demonstration project showcasing containerization patterns and deployment strategies. Feel free to use it as a reference for your own containerized applications.

## License

MIT License - see [LICENSE](LICENSE) for details.

---

*This demo application is designed to showcase containerization best practices and deployment platform comparisons in a safe, mock environment.*