# TODO: Implement Kafka Producer
import json
import time
import uuid
import random
from datetime import datetime, timezone

from kafka import KafkaProducer

SERVERS = ["web01", "web02", "db01", "app01", "cache01"]
TOPIC = "system-metrics-topic"
BOOTSTRAP_SERVERS = "localhost:29092"


def generate_metric(server_id):
    return {
        "server_id": server_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "metrics": {
            "cpu_percent": round(random.uniform(5, 95), 2),
            "memory_percent": round(random.uniform(10, 98), 2),
            "disk_io_mbps": round(random.uniform(1, 500), 2),
            "network_mbps": round(random.uniform(1, 1000), 2),
            "error_count": random.randint(0, 5)
        },
        "message_uuid": str(uuid.uuid4())
    }


def main():
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    print("Productor iniciado. Enviando métricas a Kafka...")

    try:
        while True:
            server_id = random.choice(SERVERS)
            message = generate_metric(server_id)

            producer.send(TOPIC, value=message)
            producer.flush()

            print(f"Enviado: {message}")

            time.sleep(1)

    except KeyboardInterrupt:
        print("Productor detenido manualmente.")
    except Exception as e:
        print(f"Error en el productor: {e}")
    finally:
        producer.close()


if __name__ == "__main__":
    main()