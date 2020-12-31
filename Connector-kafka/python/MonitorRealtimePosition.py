"""
    读取kafka的用户操作数据并打印
"""
from kafka import KafkaConsumer

topic = 'vehicle-order'
bootstrap_servers = ['linux01:9092']

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset='latest',
)

for msg in consumer:
    print(msg.value.decode('utf-8').encode('utf-8').decode('unicode_escape'))
