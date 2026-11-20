# 🚀 SecureOps: End-to-End Automated DevOps & GitOps Platform

[![CI/CD Pipeline](https://github.com/lok-02498/Devops_Capstone_Project/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/lok-02498/Devops_Capstone_Project/actions)
[![Docker](https://img.shields.io/badge/Containerized-Docker-blue.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Orchestrated-Kubernetes-326CE5.svg)](https://kubernetes.io/)
[![Security](https://img.shields.io/badge/Security-Trivy%20%7C%20Bandit-green.svg)](https://aquasecurity.github.io/trivy/)
[![License](https://img.shields.io/badge/Project-B.Tech%20Capstone-orange.svg)](#)

---

## 📌 Executive Summary
**SecureOps** is an enterprise-grade, end-to-end DevOps automation platform designed for modern cloud-native applications. It automates the software delivery lifecycle from code commit to zero-downtime production deployment with built-in security (DevSecOps), infrastructure as code (IaC), container orchestration, observability, and automated disaster recovery.

---

## 🏗️ High-Level System Architecture

```text
  Developer Push
        │
        ▼
┌──────────────┐     ┌────────────────────────────────────────────────────────┐
│ GitHub Repo  │ ──► │                   GitHub Actions CI/CD                 │
└──────────────┘     │  1. Flake8 Linting ──► 2. Pytest Unit Testing          │
                     │  3. SAST Scan (Bandit) ──► 4. Trivy Vulnerability Scan │
                     │  5. Multi-Stage Docker Build ──► 6. K8s Dry-Run Check  │
                     └───────────────────────────┬────────────────────────────┘
                                                 │
                                                 ▼
                             ┌───────────────────────────────────────┐
                             │    Kubernetes Production Cluster      │
                             │  ┌─────────────────────────────────┐  │
                             │  │ Deployment (v1.0.0 Stable)      │  │
                             │  │ Deployment (v2.0.0 Canary)      │  │
                             │  │ Horizontal Pod Autoscaler (HPA) │  │
                             │  │ ConfigMaps & Encrypted Secrets  │  │
                             │  └────────────────┬────────────────┘  │
                             └───────────────────┼───────────────────┘
                                                 │ Scrapes /metrics
                                                 ▼
                             ┌───────────────────────────────────────┐
                             │       Observability Stack             │
                             │  • Prometheus Metrics Engine          │
                             │  • Structured JSON System Logs        │
                             └───────────────────────────────────────┘
```

---

## 🧰 Technology Stack

| Domain | Technology / Tool | Implementation Purpose |
| :--- | :--- | :--- |
| **Version Control** | Git & GitHub | Branching strategies, semantic commits, triggers |
| **Microservice App** | Python (Flask / Gunicorn) | Task Manager REST API, `/health` probes, `/metrics` exporter |
| **Testing** | Pytest | Automated regression & unit test suite |
| **Containerization** | Docker (Multi-stage build) | Minimal image footprint, non-root security user |
| **Security (DevSecOps)** | Trivy, Bandit | SAST scanning, CVE detection, container hardening |
| **CI/CD Automation** | GitHub Actions | Automated build, test, scan, and delivery pipelines |
| **Infrastructure as Code** | Terraform | Declarative Kubernetes namespace, secrets, and config provisioning |
| **Orchestration** | Kubernetes | High availability, self-healing, rolling updates, HPA |
| **Advanced Deployment** | Canary Deployment | Zero-downtime progressive traffic split (75/25) & instant rollback |
| **Observability** | Prometheus | Real-time telemetry, latency histograms, error counters |

---

## Quick Start: Step-by-Step Execution Guide

### Step 1: Run Unit Tests Locally
```powershell
# Install requirements
pip install -r app/requirements.txt

# Run test suite
python -m pytest tests/ -v
```

### Step 2: Run Multi-Container Stack via Docker Compose
```powershell
# Build and launch application and Prometheus
docker compose up --build -d

# Verify running containers
docker compose ps
```
- Web Application UI: [http://localhost:5000](http://localhost:5000)
- Prometheus Telemetry: [http://localhost:9090](http://localhost:9090)

### Step 3: Deploy to Kubernetes
```powershell
# 1. Create production namespace
kubectl apply -f k8s/base/namespace.yaml

# 2. Deploy ConfigMaps and Secrets
kubectl apply -f k8s/base/configmap-secrets.yaml

# 3. Deploy the application workload and Service
kubectl apply -f k8s/base/deployment.yaml
kubectl apply -f k8s/base/service.yaml
kubectl apply -f k8s/base/hpa.yaml

# 4. Verify Pod status
kubectl get pods -n secureops-prod
kubectl get svc -n secureops-prod
```
Access the application on NodePort: [http://localhost:30080](http://localhost:30080).

### Step 4: Execute Canary Deployment & Traffic Splitting
```powershell
# 1. Deploy the v2.0.0 Canary workload
kubectl apply -f k8s/canary/deployment-canary.yaml

# 2. Run the automated traffic splitting evaluation script
powershell -File k8s/canary/test-canary.ps1
```

### Step 5: Provision with Terraform (IaC)
```powershell
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
```

---

## 📸 Academic Evidence & Screenshot Checklist

Take screenshots at each of the following milestone steps for your capstone document:

1. **Local Test Execution**: Output of `python -m pytest tests/ -v` showing all 5 tests passed.
2. **Docker Multi-Stage Build**: Terminal output of `docker compose up --build -d`.
3. **Web Application Dashboard**: Browser view of `http://localhost:5000` showing Pod Hostname and Healthy status.
4. **DevSecOps Trivy Scan**: Terminal or GitHub Actions log of Trivy scanning the container image.
5. **GitHub Actions CI/CD Pipeline**: GitHub UI showing all 4 workflow stages with green checkmarks.
6. **Kubernetes Deployment & Pods**: Terminal output of `kubectl get all -n secureops-prod`.
7. **Canary Traffic Verification**: Terminal output of `powershell -File k8s/canary/test-canary.ps1` demonstrating traffic distribution.
8. **Prometheus Metrics Dashboard**: Browser view of `http://localhost:9090` querying `http_requests_total`.
9. **Terraform Apply Execution**: Terminal output of `terraform apply` successfully creating resources.

---

## 📁 Repository Directory Structure

```text
Devops_project/
├── .github/
│   └── workflows/
│       └── ci-cd.yml             # Complete 4-stage GitHub Actions CI/CD pipeline
├── app/
│   ├── main.py                   # Flask REST API, probes & Prometheus instrumentation
│   └── requirements.txt          # Python dependencies
├── tests/
│   └── test_main.py              # Automated unit tests for Pytest
├── k8s/
│   ├── base/
│   │   ├── namespace.yaml         # Production namespace definition
│   │   ├── configmap-secrets.yaml # Decoupled configs & encrypted secrets
│   │   ├── deployment.yaml        # High-availability Deployment with probes
│   │   ├── service.yaml           # NodePort service definition (30080)
│   │   └── hpa.yaml               # Horizontal Pod Autoscaler configuration
│   ├── canary/
│   │   ├── deployment-canary.yaml # Canary v2.0.0 deployment
│   │   └── test-canary.ps1        # Canary progressive verification script
│   └── monitoring/
│       └── prometheus-deployment.yaml # In-cluster Prometheus deployment
├── terraform/
│   ├── main.tf                   # Declarative IaC resource definitions
│   ├── variables.tf              # Configurable infrastructure variables
│   └── outputs.tf                # IaC output declarations
├── docs/
│   ├── CAPSTONE_PROJECT_REPORT.md# Academic report template for ZOSIMA
│   └── screenshots/              # Folder to store presentation screenshots
├── Dockerfile                    # Production multi-stage secure container build
├── .dockerignore                 # Container build exclusion rules
├── docker-compose.yml            # Multi-container local orchestration
├── prometheus.yml                # Prometheus scraping metrics configuration
└── README.md                     # Comprehensive project documentation
```
