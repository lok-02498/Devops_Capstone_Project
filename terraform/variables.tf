variable "namespace" {
  description = "Kubernetes namespace for production workloads"
  type        = string
  default     = "secureops-terraform-prod"
}

variable "environment" {
  description = "Target deployment environment"
  type        = string
  default     = "production"
}

variable "db_secret_key" {
  description = "Database encryption key"
  type        = string
  default     = "ProductionSecretKey2026Terraform"
  sensitive   = true
}

variable "api_token" {
  description = "Security API token"
  type        = string
  default     = "Bearer-terraform-managed-token-2026"
  sensitive   = true
}
