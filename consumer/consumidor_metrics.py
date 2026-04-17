import os
import json
import time

from kafka import KafkaConsumer
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID")

MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_RAW_COLLECTION = os.getenv("MONGO_RAW_COLLECTION")
MONGO_KPI_COLLECTION = os.getenv("MONGO_KPI_COLLECTION")

WINDOW_SIZE = 20


def calculate_kpis(messages, window_duration_seconds):
    total_cpu = sum(m["metrics"]["cpu_percent"] for m in messages)
    total_memory = sum(m["metrics"]["memory_percent"] for m in messages)
    total_disk = sum(m["metrics"]["disk_io_mbps"] for m in messages)
    total_network = sum(m["metrics"]["network_mbps"] for m in messages)
    total_errors = sum(m["metrics"]["error_count"] for m in messages)

    message_count = len(messages)
    processing_rate = message_count / window_duration_seconds if window_duration_seconds > 0 else 0

    return {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "window_duration_seconds": round(window_duration_seconds, 2),
        "message_count": message_count,
        "kpis": {
            "avg_cpu_percent": round(total_cpu / message_count, 2),
            "avg_memory_percent": round(total_memory / message_count, 2),
            "avg_disk_io_mbps": round(total_disk / message_count, 2),
            "avg_network_mbps": round(total_network / message_count, 2),
            "total_error_count": total_errors,
            "processing_rate_msgs_per_sec": round(processing_rate, 2)
        }
    }


def main():
    mongo_client = MongoClient(MONGO_CONNECTION_STRING)
    db = mongo_client[MONGO_DB_NAME]
    raw_collection = db[MONGO_RAW_COLLECTION]
    kpi_collection = db[MONGO_KPI_COLLECTION]

    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    print("Consumidor iniciado. Esperando mensajes...")

    window_messages = []
    window_start_time = None

    try:
        for message in consumer:
            data = message.value

            raw_collection.insert_one(data)
            print(f"Insertado en RAW: {data}")

            if not window_messages:
                window_start_time = time.time()

            window_messages.append(data)

            if len(window_messages) == WINDOW_SIZE:
                window_duration = time.time() - window_start_time
                kpi_document = calculate_kpis(window_messages, window_duration)
                kpi_collection.insert_one(kpi_document)

                print(f"KPI insertado: {kpi_document}")

                window_messages = []
                window_start_time = None

    except KeyboardInterrupt:
        print("Consumidor detenido manualmente.")
    except Exception as e:
        print(f"Error en el consumidor: {e}")
    finally:
        consumer.close()
        mongo_client.close()


if __name__ == "__main__":
    main()