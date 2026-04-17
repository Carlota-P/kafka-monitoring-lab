# Evidencias
Evidencias del funcionamiento del pipeline de monitorización implementado con **Kafka, Python y MongoDB Atlas**.

El sistema desarrollado cumple con los siguientes objetivos:
- Generación de métricas simuladas de varios servidores
- Envío de mensajes a Kafka
- Consumo de mensajes desde Python
- Almacenamiento de métricas en bruto en MongoDB Atlas
- Cálculo de KPIs agregados cada 20 mensajes
- Almacenamiento de KPIs en una segunda colección de MongoDB

---

## 1. Productor publicando métricas en Kafka
En la siguiente evidencia se muestra el funcionamiento del script productor (`producer/productor_metrics.py`), generando métricas simuladas para los servidores definidos en la práctica y enviándolas correctamente al tópico de Kafka.

Cada mensaje incluye:
- `server_id`
- `timestamp_utc`
- `metrics`
- `message_uuid`

Además, se observa en consola que los mensajes se generan de forma continua y se publican sin errores.
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/acbbde6e-d325-4fc8-a3f6-3bdd870c3b64" />

---

## 2. Consumidor leyendo mensajes e insertando en MongoDB

En esta evidencia se muestra el funcionamiento del script consumidor (`consumer/consumidor_metrics.py`).

El consumidor:
- se conecta al tópico de Kafka
- recibe los mensajes publicados por el productor
- inserta cada mensaje en la colección `system_metrics_raw`
- calcula una ventana tumbling cada 20 mensajes
- genera e inserta los KPIs en `system_metrics_kpis`

En la consola puede verse tanto la inserción de datos RAW como la generación de documentos KPI.
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0ac56153-be20-43ba-9d2d-b807634784cb" />

---

## 4. Evidencia de almacenamiento de KPIs en MongoDB Atlas

En esta evidencia se muestra la colección `system_metrics_kpis` dentro de la base de datos `monitoring`.

Cada documento KPI incluye:

- `timestamp`
- `window_duration_seconds`
- `message_count`
- objeto `kpis`

Dentro del bloque `kpis` se almacenan los indicadores calculados para cada ventana de 20 mensajes:

- promedio de CPU
- promedio de memoria
- promedio de disco
- promedio de red
- suma de errores
- tasa de procesamiento en mensajes por segundo

Esto confirma que la lógica de agregación y cálculo de KPIs se ejecuta correctamente.
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a27c64bb-5bc2-4f5d-b9d5-b497182d195b" />

---

## 3. Evidencia de almacenamiento RAW en MongoDB Atlas

En la siguiente imagen se observa la colección `system_metrics_raw` dentro de la base de datos `monitoring` en MongoDB Atlas.

Se puede comprobar que los documentos almacenados contienen correctamente los datos originales consumidos desde Kafka, incluyendo:

- identificador del servidor
- marca temporal en UTC
- objeto de métricas
- identificador único del mensaje

Esto demuestra que el almacenamiento en bruto de los eventos funciona correctamente.
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/804db608-74d9-48a9-82e0-357860470b3d" />

## 6. Observaciones finales

Durante el desarrollo se configuró:

- Kafka mediante Docker Compose en entorno local
- MongoDB Atlas como base de datos remota
- variables de entorno mediante archivo `.env`
- conexión entre productor, consumidor, Kafka y MongoDB

