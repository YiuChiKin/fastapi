resource "helm_release" "stock_api" {
  name             = "stock-api"
  namespace        = var.namespace
  create_namespace = true

  chart = "${path.module}/../docs/stock-api-0.1.0.tgz"

  set_sensitive {
    name  = "secret.finnhubApiKey"
    value = var.finnhub_api_key
  }

  set {
    name  = "image.repository"
    value = "localhost/stock-api"
  }

  set {
    name  = "image.tag"
    value = var.image_tag
  }

  # Required for locally built images — Kubernetes must not try to pull from a registry
  set {
    name  = "image.pullPolicy"
    value = "Never"
  }
}
