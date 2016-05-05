import os
import json
import ConfigParser
import logging

import serial
import paho.mqtt.publish as publish



config = ConfigParser.ConfigParser()
config.read('config')

xbee_dev = config.get('settings', 'xbee-serial-id')
baudrate = config.getint('settings', 'baudrate')


logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    filename=config.get('settings', 'log-path'),
                    level=logging.DEBUG)

def read_xbee():
    if not os.path.exists(xbee_dev):
        logging.error('Serial device: %s does not exist' % (xbee_dev))
    xbee = serial.Serial(xbee_dev, baudrate)

    while True:
        try:
            yield xbee.readline()
        except Exception as ex:
            logging.warning('Exception: %s' % (ex))





for line in read_xbee():
    try:
        data = json.loads(line)
        key, value = data.keys()[0], data[data.keys()[0]]
        logging.info('publishing: xbee/%s/%s' % (key, value))

        publish.single("xbee/%s" % (key),  
                value, 
                hostname="192.168.1.15", 
                client_id="xbee_bridge", 
                auth={"username":"xbee"})

    except ValueError as ex:
        continue



