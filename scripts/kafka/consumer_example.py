"""
Kafka Consumer Example
Consumes agricultural events from a Kafka topic.
Requires: confluent-kafka
"""
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

try:
    from confluent_kafka import Consumer
    HAS_KAFKA = True
except ImportError:
    HAS_KAFKA = False
    logging.warning("confluent_kafka module not found. Running in MOCK mode.")

def main():
    if not HAS_KAFKA:
        logging.info("[MOCK] Consumer started. Waiting for messages... (Press Ctrl+C to stop)")
        return

    conf = {
        'bootstrap.servers': 'localhost:29092',
        'group.id': 'agric-analytics-group',
        'auto.offset.reset': 'earliest'
    }

    c = Consumer(conf)
    c.subscribe(['harvest_logs'])

    try:
        while True:
            msg = c.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                logging.error(f"Consumer error: {msg.error()}")
                continue

            logging.info(f'Received message: {msg.value().decode("utf-8")}')

    except KeyboardInterrupt:
        pass
    finally:
        c.close()

if __name__ == '__main__':
    main()
