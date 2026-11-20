output "namespace_name" {
  description = "The created Kubernetes namespace name"
  value       = kubernetes_namespace.prod_namespace.metadata[0].name
}

output "config_map_name" {
  description = "Name of the provisioned ConfigMap"
  value       = kubernetes_config_map.app_config.metadata[0].name
}

output "secret_name" {
  description = "Name of the provisioned Secret"
  value       = kubernetes_secret.app_secret.metadata[0].name
}
