import consul
from .config import CONSUL_HOST, CONSUL_PORT, URL_PREFIX

def register_in_consul():
    c = consul.Consul(host=CONSUL_HOST, port=CONSUL_PORT)
    c.agent.service.register('won', tags=["home-automation"], check=consul.Check.http(url='https://home.kabala.tech/{}/health'.format(URL_PREFIX), interval="10s", timeout="1s"))
