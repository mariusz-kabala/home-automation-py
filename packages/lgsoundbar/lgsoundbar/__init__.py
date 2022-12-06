import tornado.platform.asyncio
import tornado.ioloop
import tornado.web
from . import routes
from .logger import logger
from .soundbar import Soundbar
from .mqtt import Mqtt
from .config import HTTP_PORT

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
        (r"/settings", routes.SettingsHandler),
        (r"/eq", routes.EqHandler),
        (r"/info", routes.InfoHandler),
        (r"/func", routes.FuncHandler),
        (r"/play", routes.PlayHandler),
        (r"/product", routes.ProductHandler),
        (r"/c4a", routes.C4aHandler),
        (r"/radio", routes.RadioHandler),
        (r"/ap", routes.ApHandler), # nie dziala
        (r"/update", routes.UpdateHandler),
        (r"/build", routes.BuildHandler),
        (r"/option", routes.OptionHandler),
        (r"/mac", routes.MacHandler),
        (r"/mem-mon", routes.MemMonHandler),
        (r"/test", routes.TestHandler),
        (r"/set/night-mode", routes.TestHandler),
        (r"/set/volume", routes.SetVolume),
        (r"/set/mute", routes.SetMute),
    ], soundbar=sb)

def start():
    app = make_app()
    app.listen(HTTP_PORT)

    logger.info('Application started on port {}'.format(HTTP_PORT))
    
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    start()
