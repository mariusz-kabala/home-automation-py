resource "docker_container" "won" {
  name  = "won"
  image = "${var.DOCKER_REGISTRY}/won:${var.tag}"
  restart = "always"
  network_mode = "host"

  # networks_advanced {
  #     name = var.network_name
  # }

  labels {
    label = "traefik.enable"
    value = "true"
  }

  labels {
    label = "traefik.http.routers.won.rule"
    value = "Host(`${var.app_domain}`) && PathPrefix(`/${var.url_prefix}`)"
  }

  labels {
    label = "traefik.http.services.won.loadbalancer.server.port"
    value = "${var.http_port}"
  }

  env = [
      "MQTT_HOST=${var.mqtt_host}",
      "HTTP_PORT=${var.http_port}",
      "URL_PREFIX=${var.url_prefix}",
      "CONSUL_HOST=${var.consul_host}",
      "CONSUL_PORT=${var.consul_port}"
  ]
  dns = [
    "192.168.50.160"
  ]
}
