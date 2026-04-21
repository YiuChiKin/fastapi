resource "helm_release" "stock_api" {
  name             = "stock-api"
  namespace        = var.namespace
  create_namespace = true

  # Pulls the chart from the GitHub Pages Helm repository (no redirect issues)
  repository = "https://YiuChiKin.github.io/fastapi"
  chart      = "stock-api"
  version    = var.chart_version

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
