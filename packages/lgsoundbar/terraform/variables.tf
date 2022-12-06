variable "tag" {}


variable "DOCKER_REGISTRY_USERNAME" {}

variable "DOCKER_REGISTRY_PASSWORD" {}

variable "DOCKER_REGISTRY" {
    default = "docker-registry.kabala.tech"
}

variable "app_domain" {}

variable "docker_host" {}

variable "consul_host" {}

variable "consul_port" {
  default = "8500"
}

variable "network_name" {}

variable "mqtt_host" {}

variable "device_ip" {}

variable "http_port" {
  default = "8888"
}
