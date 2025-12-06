"""
Kafka Producer Example
Publishes agricultural events to a Kafka topic.
Requires: confluent-kafka
"""
import json
import time
import random
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Mock Kafka Producer if library missing
try:
    from confluent_kafka import Producer
    HAS_KAFKA = True
except ImportError:
    HAS_KAFKA = False
    logging.warning("confluent_kafka module not found. Running in MOCK mode.")

def delivery_report(err, msg):
    if err is not None:
        logging.error(f'Message delivery failed: {err}')
    else:
        logging.info(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def main():
    conf = {'bootstrap.servers': 'localhost:29092'}
    
    if HAS_KAFKA:
        p = Producer(conf)
    else:
        p = None

    topics = ['commodity_prices', 'weather_alerts', 'harvest_logs']

    try:
        for i in range(5):
            # Create a mock event
            data = {
                'event_id': f'EVT-{i}',
                'timestamp': datetime.now().isoformat(),
                'type': 'HarvestRecorded',
                'payload': {
                    'farmer_id': f'FMR{random.randint(100,200)}',
                    'quantity': random.uniform(10, 500)
                }
            }
            
            msg_str = json.dumps(data)
            topic = 'harvest_logs'
            
            if HAS_KAFKA:
                p.produce(topic, msg_str.encode('utf-8'), callback=delivery_report)
                p.poll(0)
            else:
                logging.info(f"[MOCK] Produced to {topic}: {msg_str}")
            
            time.sleep(1)

        if HAS_KAFKA:
            p.flush()
            
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
