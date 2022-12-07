import tornado.platform.asyncio
import tornado.ioloop
import tornado.web
from . import routes
from .logger import logger
from .soundbar import Soundbar
from .mqtt import Mqtt
from .consul import register_in_consul
from .config import HTTP_PORT, URL_PREFIX

def make_app():
    mqtt = Mqtt({
        '/get/settings': lambda : sb.get_settings(),
        '/get/eq': lambda : sb.get_eq(),
        '/get/info': lambda : sb.get_info(),
        '/get/func': lambda : sb.get_func(),
        '/get/product': lambda : sb.get_product_info(),
        '/get/option': lambda : sb.get_option_info(),
        '/get/mac': lambda : sb.get_mac_info(),
        '/get/build': lambda : sb.get_build_info(),
        '/get/update': lambda : sb.get_update_info()
    })

    sb = Soundbar(lambda msg, payload : mqtt.publish(msg, payload))

    mqtt.subscribeToTopics()
    mqtt.connect()

    return tornado.web.Application([
        (r"/{}/health".format(URL_PREFIX), routes.HealthCheck),
        (r"/{}/settings".format(URL_PREFIX), routes.SettingsHandler),
        (r"/{}/eq".format(URL_PREFIX), routes.EqHandler),
        (r"/{}/info".format(URL_PREFIX), routes.InfoHandler),
        (r"/{}/func".format(URL_PREFIX), routes.FuncHandler),
        (r"/{}/play".format(URL_PREFIX), routes.PlayHandler),
        (r"/{}/product".format(URL_PREFIX), routes.ProductHandler),
        (r"/{}/c4a".format(URL_PREFIX), routes.C4aHandler),
        (r"/{}/radio".format(URL_PREFIX), routes.RadioHandler),
        (r"/{}/ap".format(URL_PREFIX), routes.ApHandler), # nie dziala
        (r"/{}/update".format(URL_PREFIX), routes.UpdateHandler),
        (r"/{}/build".format(URL_PREFIX), routes.BuildHandler),
        (r"/{}/option".format(URL_PREFIX), routes.OptionHandler),
        (r"/{}/mac".format(URL_PREFIX), routes.MacHandler),
        (r"/{}/mem-mon".format(URL_PREFIX), routes.MemMonHandler),
        (r"/{}/test".format(URL_PREFIX), routes.TestHandler),
        (r"/{}/set/night-mode".format(URL_PREFIX), routes.TestHandler),
        (r"/{}/set/volume".format(URL_PREFIX), routes.SetVolume),
        (r"/{}/set/mute".format(URL_PREFIX), routes.SetMute),
    ], soundbar=sb)

def start():
    app = make_app()
    register_in_consul()
    app.listen(HTTP_PORT)

    logger.info('Application started on port {}'.format(HTTP_PORT))
    
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    start()
