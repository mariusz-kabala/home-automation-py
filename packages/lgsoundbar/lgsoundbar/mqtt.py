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

        match msg:
            case "SPK_LIST_VIEW_INFO":
                self.mqttClient.publish('{}/info'.format(MQTT_TOPIC), json.dump(payload))

            case "FUNC_VIEW_INFO":
                self.mqttClient.publish('{}/func'.format(MQTT_TOPIC), json.dump(payload))

            case 'SETTING_VIEW_INFO':
                self.mqttClient.publish('{}/settings'.format(MQTT_TOPIC), json.dump(payload))

            case 'PRODUCT_INFO':
                self.mqttClient.publish('{}/product'.format(MQTT_TOPIC), json.dump(payload))

            case 'BUILD_INFO_DEV':
                self.mqttClient.publish('{}/build'.format(MQTT_TOPIC), json.dump(payload))
            
            case 'MAC_INFO_DEV':
                self.mqttClient.publish('{}/mac'.format(MQTT_TOPIC), json.dump(payload))

            case 'EQ_VIEW_INFO':
                self.mqttClient.publish('{}/eq'.format(MQTT_TOPIC), json.dump(payload))
