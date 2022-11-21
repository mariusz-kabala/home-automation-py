from .soundbar import Soundbar
import asyncio
import tornado.web

sb = Soundbar()

class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        print('got GET Request')
        result = await sb.get_settings()
        print("result", result)
        self.write(result)

def make_app():
    return tornado.web.Application([
        (r"/settings", MainHandler),
    ])

def onMessage(json):
    print(json)
    print(type(json))

async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()
    # print('start!')
    # speaker = temescal.temescal("192.168.50.18", callback=onMessage)
    # speaker.get_info()

    # app.run(debug=False, use_reloader=False, port=8333, host='0.0.0.0')

# @app.route('/settings', methods=['GET',])
# async def settings():
#     result = await sb.get_settings()
    
    # return (result, 200)

def start():
    asyncio.run(main())

if __name__ == '__main__':
    asyncio.run(main())
