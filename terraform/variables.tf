variable "kube_context" {
  type        = string
  description = "kubectl context name to use (e.g. docker-desktop or minikube)"
}

variable "finnhub_api_key" {
  type        = string
  sensitive   = true
  description = "Finnhub API key injected into the Kubernetes Secret"
}

variable "image_tag" {
  type        = string
  default     = "latest"
  description = "Docker image tag to deploy"
}

variable "namespace" {
  type        = string
  default     = "default"
  description = "Kubernetes namespace for the Helm release"
}

variable "chart_version" {
  type        = string
  default     = "0.1.0"
  description = "Helm chart version to deploy from GitHub Releases"
}
