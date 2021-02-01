"""
    读取kafka中订单数据并转换为Wgs84坐标
"""
from kafka import KafkaConsumer
from kafka import KafkaProducer
from json import *
from com.gis.rookie.position.entity.CoordinateTransform import gcj02towgs84
from com.gis.rookie.position.entity.VehicleOrder import VehicleOrder

import json


input_topic = 'vehicle-order'
output_topic = 'vehicle-order-wgs'
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
        orderId = dict_json['orderId']
        startTimeStamp = dict_json['startTimeStamp']
        endTimeStamp = dict_json['endTimeStamp']
        getOnLongitude = dict_json['getOnLongitude']
        getOnLatitude = dict_json['getOnLatitude']
        getOffLongitude = dict_json['getOffLongitude']
        getOffLatitude = dict_json['getOffLatitude']
        value = dict_json['value']
        startTime = dict_json['startTime']
        endTime = dict_json['endTime']
        vehicleOrder = VehicleOrder(orderId, startTimeStamp, endTimeStamp, getOnLongitude, getOnLatitude, getOffLongitude, getOffLatitude, value, startTime, endTime)
        return vehicleOrder


def kafkaProducter(wgsVehicleOrder):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda x: dumps(x).encode('utf-8'))
    order_dict = objectToDict(wgsVehicleOrder)
    producer.send(output_topic, value=order_dict)


def coordinateTransform(vehicleOrder):
    getOnPosition = gcj02towgs84(vehicleOrder.getOnLongitude, vehicleOrder.getOnLatitude)
    getOffPositioin = gcj02towgs84(vehicleOrder.getOffLongitude, vehicleOrder.getOffLatitude)
    wgsVehicleOrder = VehicleOrder(vehicleOrder.orderId, vehicleOrder.startTimeStamp, vehicleOrder.endTimeStamp,
                                   getOnPosition[0], getOnPosition[1], getOffPositioin[0], getOnPosition[1],
                                   vehicleOrder.value, vehicleOrder.startTime, vehicleOrder.endTime)
    return wgsVehicleOrder

def objectToDict(vehicleOrder):
    return {
        'orderId': vehicleOrder.orderId,
        'startTimeStamp': vehicleOrder.startTimeStamp,
        'endTimeStamp': vehicleOrder.endTimeStamp,
        'getOnLongitude': vehicleOrder.getOnLongitude,
        'getOnLatitude': vehicleOrder.getOnLatitude,
        'getOffLongitude': vehicleOrder.getOffLongitude,
        'getOffLatitude': vehicleOrder.getOffLatitude,
        'value': vehicleOrder.value,
        'startTime': vehicleOrder.startTime,
        'endTime': vehicleOrder.endTime
    }

if __name__ == '__main__':
    var = 1
    while var == 1:
        vehicleOrder = kafkaConsumer()
        wgsVehicleOrder = coordinateTransform(vehicleOrder)
        kafkaProducter(wgsVehicleOrder)
