terraform {
  required_version = ">= 1.0.0"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.26.0"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

# 1. Provision Production Namespace
resource "kubernetes_namespace" "prod_namespace" {
  metadata {
    name = var.namespace
    labels = {
      environment = var.environment
      managed_by  = "terraform"
      project     = "devops-capstone"
    }
  }
}

# 2. Provision ConfigMap for Application Configuration
resource "kubernetes_config_map" "app_config" {
  metadata {
    name      = "secureops-config-tf"
    namespace = kubernetes_namespace.prod_namespace.metadata[0].name
  }

  data = {
    APP_ENV        = var.environment
    LOG_LEVEL      = "INFO"
    ENABLE_METRICS = "true"
  }
}

# 3. Provision Secret for Secure Credentials
resource "kubernetes_secret" "app_secret" {
  metadata {
    name      = "secureops-secrets-tf"
    namespace = kubernetes_namespace.prod_namespace.metadata[0].name
  }

  data = {
    DATABASE_SECRET_KEY = var.db_secret_key
    API_AUTH_TOKEN      = var.api_token
  }

  type = "Opaque"
}
