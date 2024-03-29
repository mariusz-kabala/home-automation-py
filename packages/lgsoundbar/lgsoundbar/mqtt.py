import paho.mqtt.client as mqtt
from .logger import logger
from .config import MQTT_HOST, MQTT_PORT, MQTT_TOPIC
import json
from typing import Callable
import os

Subscriptions = dict[str, Callable]

class Mqtt:
    def __init__(self, subscriptions: Subscriptions):
        self.client = mqtt.Client()
        self.subscriptions = subscriptions
        # self.client.on_connect = self.onConnect 
        
    def onConnect(self):
        logger.info('Connected to mqtt server')

    def onDisconnect(self):
        logger.error('Lost connection with mqtt server')

    def connect(self):
        logger.info('Connecting to {host} on port {port}'.format(host=MQTT_HOST, port=MQTT_PORT))
        self.client.connect_async(MQTT_HOST, MQTT_PORT, 60)
        self.client.loop_start()

    def getTopic(self, topic):
        return '{prefix}{topic}'.format(prefix = MQTT_TOPIC, topic = topic)

    def subscribeToTopics(self):
        topics = list(map(lambda topic : (self.getTopic(topic), 0), self.subscriptions.keys()))
        self.client.subscribe(topics)

        for topic, func in self.subscriptions.items():
            self.client.message_callback_add(self.getTopic(topic), func)
        
    def publish(self, msg: str, payload):
        if not self.client.is_connected:
            return

        logger.info("Publishing a new msg: {}".format(msg))
        
        match msg:
            case "SPK_LIST_VIEW_INFO":
                self.client.publish('{}/info'.format(MQTT_TOPIC), json.dumps(payload), retain=True)

            case "FUNC_VIEW_INFO":
                self.client.publish('{}/func'.format(MQTT_TOPIC), json.dumps(payload), retain=True)

            case 'SETTING_VIEW_INFO':
                self.client.publish('{}/settings'.format(MQTT_TOPIC), json.dumps(payload), retain=True)

            case 'PRODUCT_INFO':
                self.client.publish('{}/product'.format(MQTT_TOPIC), json.dumps(payload))

            case 'BUILD_INFO_DEV':
                self.client.publish('{}/build'.format(MQTT_TOPIC), json.dumps(payload))
            
            case 'MAC_INFO_DEV':
                self.client.publish('{}/mac'.format(MQTT_TOPIC), json.dumps(payload))

            case 'EQ_VIEW_INFO':
                self.client.publish('{}/eq'.format(MQTT_TOPIC), json.dumps(payload), retain=True)
