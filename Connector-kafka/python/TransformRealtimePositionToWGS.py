"""
    读取kafka中车辆实时位置数据，转换为Wgs84坐标
"""
import math

from kafka import KafkaConsumer
from kafka import KafkaProducer
from json import *
from com.gis.rookie.position.entity.CoordinateTransform import gcj02towgs84
from com.gis.rookie.position.entity.VehiclePosition import *

import json

input_topic = 'vehicle-position'
output_topic = 'vehicle-gps'
bootstrap_servers = ['linux01:9092']

consumer = KafkaConsumer(
   input_topic,
   bootstrap_servers=bootstrap_servers,
   auto_offset_reset='latest',
)


def kafkaConsumer():
    for msg in consumer:
        message = msg.value.decode('utf-8').encode('utf-8').decode('unicode_escape')
        dict_json = json.loads(message)
        driverId = dict_json["driverId"]
        orderId = dict_json["orderId"]
        timeStamp = dict_json["timeStamp"]
        longitude = float(dict_json["longitude"])
        latitude = float(dict_json["latitude"])
        time = dict_json["time"]
        vehiclePosition = VehiclePosition(driverId, orderId, timeStamp, longitude, latitude, time)
        return vehiclePosition


def kafkaProducter(wgsPosition):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda x: dumps(x).encode('utf-8'))
    position_dict = objectToDict(wgsPosition)
    producer.send(output_topic, value=position_dict)


def coordinateTransform(vehiclePosition):
    position = gcj02towgs84(vehiclePosition.longitude, vehiclePosition.latitude)
    wgsVehiclePosition = VehiclePosition(vehiclePosition.driverId, vehiclePosition.orderId, vehiclePosition.timeStamp, position[0], position[1], vehiclePosition.time)
    return wgsVehiclePosition

def wgs84toWebMercator(vehiclePosition):
    lon = vehiclePosition.longitude
    lat = vehiclePosition.latitude
    x = lon*20037508.342789/180
    y = math.log(math.tan((90+lat)*math.pi/360))/(math.pi/180)
    y = y * 20037508.34789/180
    vehiclePosition.resetXAndY(x, y)
    return vehiclePosition


def objectToDict(vehiclePosition):
    return {
        'driverId': vehiclePosition.driverId,
        'orderId': vehiclePosition.orderId,
        'timeStamp': vehiclePosition.timeStamp,
        'longitude': vehiclePosition.longitude,
        'latitude': vehiclePosition.latitude,
        'time': vehiclePosition.time
    }


if __name__ == '__main__':
    var = 1
    while var == 1:
        vehiclePosition = kafkaConsumer()
        wgsPosition = coordinateTransform(vehiclePosition)
        utmPosition = wgs84toWebMercator(wgsPosition)
        kafkaProducter(utmPosition)

