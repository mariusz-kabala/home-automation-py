resource "docker_container" "lgsoundbar" {
  name  = "lgsoundbar"
  image = "${var.DOCKER_REGISTRY}/lgsoundbar:${var.tag}"
  restart = "always"

  networks_advanced {
      name = var.network_name
  }

  labels {
    label = "traefik.enable"
    value = "true"
  }

  labels {
    label = "traefik.http.routers.soundbar.rule"
    value = "Host(`${var.app_domain}`) && PathPrefix(`/soundbar`)"
  }

  labels {
    label = "traefik.http.services.soundbar.loadbalancer.server.port"
    value = "${var.http_port}"
  }

  env = [
      "MQTT_HOST=${var.mqtt_host}",
      "DEVICE_IP=${var.device_ip}",
      "HTTP_PORT=${var.http_port}",
      "CONSUL_HOST=${var.consul_host}",
      "CONSUL_PORT=${var.consul_port}"
  ]
  dns = [
    "192.168.50.160"
  ]
}
