
import temescal
import asyncio

class Soundbar:
    futures = {}

    def __init__(self):
        self.speaker = temescal.temescal("192.168.50.18", callback=self.onMessage)

    def onMessage(self, json):
        msg = json["msg"]

        print("got message")
        print(msg, self.futures["SETTING_VIEW_INFO"])

        if (msg in self.futures.keys()):
            for future in self.futures.get(msg):
                future.set_result(json["data"])
                print("future data set")

            self.futures.get(msg).clear()


    def get_settings(self):
        future = asyncio.get_running_loop().create_future()

        if "get_settings" not in self.futures.keys():
            self.futures["SETTING_VIEW_INFO"] = []

        self.futures["SETTING_VIEW_INFO"].append(future)
        print ("returning future")

        self.speaker.get_settings()

        return future
