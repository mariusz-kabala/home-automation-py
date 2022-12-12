resource "docker_container" "won" {
  name  = "won"
  image = "${var.DOCKER_REGISTRY}/won:${var.tag}"
  restart = "always"
  network_mode = "host"

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
