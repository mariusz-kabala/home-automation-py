
import temescal
import asyncio
import paho.mqtt.client as mqtt
from .config import DEVICE_IP
from typing import Callable, Any

# i_curr_eq - Sound Effect:
# 19 - AI Sound Pro
# 14 - Bass Blast
# 0 - Standard
# 13 - Movie
# 6 - Music
# ----------
# i_curr_func - Input
# 1 - bluetooth
# 4 - OPT/H
# 6 - HDMI 1
# 10 - HDMI 2
# 19 - USB
# 0 - WIFI

class Soundbar:
    futures = {}

    mapper = {
        "EQ_VIEW_INFO": 'get_eq',
        "SPK_LIST_VIEW_INFO": 'get_info',
        "PLAY_INFO": "get_play",
        "FUNC_VIEW_INFO": "get_func",
        "SETTING_VIEW_INFO": "get_settings",
        "PRODUCT_INFO": "get_product_info",
        "C4A_SETTING_INFO": "get_c4a_info",
        "RADIO_VIEW_INFO": "get_radio_info",
        "SHARE_AP_INFO": "get_ap_info",
        "UPDATE_VIEW_INFO": "get_update_info",
        "BUILD_INFO_DEV": "get_build_info",
        "OPTION_INFO_DEV": "get_option_info",
        "MAC_INFO_DEV": "get_mac_info",
        "MEM_MON_DEV": "get_mem_mon_info",
        "TEST_DEV": "get_test_info"
    }

    def __init__(self, callback: Callable[[str, Any], None]):
        self.speaker = temescal.temescal(DEVICE_IP, callback=self.onDeviceMessage)
        self.loop = asyncio.get_event_loop()
        self.mqttClient = mqtt.Client()
        self.callbackFunc = callback

    def onDeviceMessage(self, json):
        msg = json["msg"]

        self.callbackFunc(msg, json["data"])

        if (msg in self.futures.keys()):
            for future in self.futures.get(msg):
                self.loop.call_soon_threadsafe(future.set_result, json["data"])
                
            self.futures.get(msg).clear()

    async def executeCommand(self, command):
        future = self.loop.create_future()

        if command not in self.futures.keys():
            self.futures[command] = []

        self.futures[command].append(future)

        func = getattr(self.speaker, self.mapper[command])

        func()

        result = await future

        return result

    async def get_eq(self):
        return await self.executeCommand("EQ_VIEW_INFO")

    async def get_info(self):
        return await self.executeCommand("SPK_LIST_VIEW_INFO")

    async def get_play(self):
        return await self.executeCommand("PLAY_INFO")

    async def get_func(self):
        return await self.executeCommand("FUNC_VIEW_INFO")

    async def get_settings(self):
        return await self.executeCommand("SETTING_VIEW_INFO")

    async def get_product_info(self):
        return await self.executeCommand("PRODUCT_INFO")

    async def get_c4a_info(self):
        return await self.executeCommand("C4A_SETTING_INFO")

    async def get_radio_info(self):
        return await self.executeCommand("RADIO_VIEW_INFO")

    async def get_ap_info(self):
        return await self.executeCommand("SHARE_AP_INFO")

    async def get_update_info(self):
        return await self.executeCommand("UPDATE_VIEW_INFO")

    async def get_build_info(self):
        return await self.executeCommand("BUILD_INFO_DEV")

    async def get_option_info(self):
        return await self.executeCommand("OPTION_INFO_DEV")

    async def get_mac_info(self):
        return await self.executeCommand("MAC_INFO_DEV")

    async def get_mem_mon_info(self):
        return await self.executeCommand("MEM_MON_DEV")

    async def get_test_info(self):
        return await self.executeCommand("TEST_DEV")
