# Kafka Monitoring Lab

## Descripción

Este proyecto implementa un pipeline de monitorización en tiempo real utilizando **Apache Kafka**, **Python** y **MongoDB Atlas**.

El sistema simula métricas de varios servidores, las publica en Kafka mediante un productor, las consume desde Python con un consumidor, las almacena en bruto en MongoDB Atlas y calcula **KPIs agregados cada 20 mensajes** mediante una ventana *tumbling*. :contentReference[oaicite:0]{index=0}

---

## Objetivo

Desarrollar un sistema completo capaz de:

- generar métricas simuladas de varios servidores
- enviarlas a Kafka
- consumirlas desde Python
- almacenarlas en MongoDB Atlas
- calcular KPIs agregados
- almacenar los KPIs en una segunda colección de MongoDB :contentReference[oaicite:1]{index=1}

---

## Tecnologías utilizadas

- **Python 3**
- **Apache Kafka**
- **MongoDB Atlas**
- **Docker Compose**
- **kafka-python**
- **pymongo**
- **python-dotenv**

---

## Estructura del proyecto

```bash
kafka-monitoring-lab/
├── consumer/
│   └── consumidor_metrics.py
├── producer/
│   └── productor_metrics.py
├── docker/
│   └── docker-compose.yml
├── docs/
│   └── evidencias.md
├── .env
├── README.md
└── requirements.txt
