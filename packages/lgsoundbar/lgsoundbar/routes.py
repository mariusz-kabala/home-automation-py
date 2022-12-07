import tornado.web
import asyncio
from datetime import datetime

class AppHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.sb = self.application.settings.get('soundbar')

class SettingsHandler(AppHandler):
    async def get(self):
        task = asyncio.create_task(self.sb.get_settings())
        result = await task
        self.write(result)

class EqHandler(AppHandler):
    async def get(self):
        task = asyncio.create_task(self.sb.get_eq())
        result = await task
        self.write(result)

    def put(self):
        json = tornado.escape.json_decode(self.request.body)

        self.sb.speaker.set_func(json.get('eq', 1))

        self.setStatus(200)
        self.finish()

class InfoHandler(AppHandler):
    async def get(self):
        task = asyncio.create_task(self.sb.get_info())
        result = await task
        self.write(result)

class FuncHandler(AppHandler):
    async def get(self):
        task = asyncio.create_task(self.sb.get_func())
        result = await task
        self.write(result)

    def put(self):
        json = tornado.escape.json_decode(self.request.body)
        
        self.sb.speaker.set_func(json.get('func', 1))

        self.setStatus(200)
        self.finish()

class PlayHandler(AppHandler):
    async def get(self):
        task = asyncio.create_task(self.sb.get_play())
        result = await task
        self.write(result)

class ProductHandler(AppHandler):
    async def get(self):
        task = asyncio.create_task(self.sb.get_product_info())
        result = await task
        self.write(result)

class C4aHandler(AppHandler):
    async def get(self):
        task = asyncio.create_task(self.sb.get_c4a_info())
        result = await task
        self.write(result)

class RadioHandler(AppHandler):
    async def get(self):
        task = asyncio.create_task(self.sb.get_radio_info())
        result = await task
        self.write(result)

class ApHandler(AppHandler):
    async def get(self):
        task = asyncio.create_task(self.sb.get_ap_info())
        result = await task
        self.write(result)

class UpdateHandler(AppHandler):
    async def get(self):
        task = asyncio.create_task(self.sb.get_update_info())
        result = await task
        self.write(result)

class BuildHandler(AppHandler):
    async def get(self):
        task = asyncio.create_task(self.sb.get_build_info())
        result = await task
        self.write(result)

class OptionHandler(AppHandler):
    async def get(self):
        task = asyncio.create_task(self.sb.get_option_info())
        result = await task
        self.write(result)

class MacHandler(AppHandler):
    async def get(self):
        task = asyncio.create_task(self.sb.get_mac_info())
        result = await task
        self.write(result)

class MemMonHandler(AppHandler):
    async def get(self):
        task = asyncio.create_task(self.sb.get_mem_mon_info())
        result = await task
        self.write(result)

class TestHandler(AppHandler):
    async def get(self):
        task = asyncio.create_task(self.sb.get_test_info())
        result = await task
        self.write(result)

class SetNightMode(AppHandler):
    def put(self):
        json = tornado.escape.json_decode(self.request.body)
        
        self.sb.speaker.set_night_mode(json.get('enabled', False))

        self.setStatus(200)
        self.finish()

class SetVolume(AppHandler):
    def put(self):
        json = tornado.escape.json_decode(self.request.body)

        self.sb.speaker.set_volume(json.get('value'), 10)

        self.setStatus(200)
        self.finish()

class SetMute(AppHandler):
    def put(self):
        json = tornado.escape.json_decode(self.request.body)
        
        self.sb.speaker.set_mute(json.get('enabled', False))

        self.setStatus(200)
        self.finish()

class HealthCheck(tornado.web.RequestHandler):
    def initialize(self):
        self.start = datetime.now()

    def get(self):
        self.setStatus(200)
        self.write({
            "status": True,
            "startedAt": self.start.strftime("%d/%m/%Y %H:%M:%S")
        })
        self.finish()
        
