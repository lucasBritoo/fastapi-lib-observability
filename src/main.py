import psutil
from datetime import datetime
import time

import logging
import os
import random
import time
from typing import Optional

import httpx
import uvicorn
from fastapi import FastAPI, Response
from opentelemetry.propagate import inject

from lib_fastapi.lib_fastapi import FastApiObservability
from lib_fastapi.lib_fastapi import PrometheusMiddleware
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from prometheus_client import REGISTRY, Counter, Gauge, Histogram

push_gateway_host = os.environ.get("PUSH_GATEWAY_HOST")
push_gateway_port = os.environ.get("PUSH_GATEWAY_PORT")
app_name= os.environ.get("APP_NAME")
app_host= os.environ.get("APP_HOST")
app_port= os.environ.get("APP_PORT")
app_version= os.environ.get("APP_VERSION")
tempo_port= os.environ.get("TEMPO_PORT")
tempo_host= os.environ.get("TEMPO_HOST")

push_gateway_url = push_gateway_host + ":" + push_gateway_port
tempo_url = 'http://' + tempo_host + ':' + tempo_port

app = FastApiObservability(path="/", name=app_name, version=app_version,
                           prometheus=True, tempo=True, tempoUrl=tempo_url).get_api_application()

REQUEST_TESTE = Counter(
    "fastapi_requests_teste", "Total count of requests by method and path.",  ["app_name"]
)

# class EndpointFilter(logging.Filter):

#     def filter(self, record: logging.LogRecord) -> bool:
#         return record.getMessage().find('GET /metrics') == -1

# logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

# Vetor para armazenar as medidas
measurements = []


@app.get('/data')
def get_system_date():
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info("Recuperando Data")
    return {"date": configs.config_settings["TEMPO_OTLP_GRPC"]}

@app.get("/cpu")
def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)  # Obtém a porcentagem de uso da CPU
    logging.info("Recuperando CPU")
    REQUEST_TESTE.labels(app_name=app_name).inc()
    return {"cpu_usage": cpu_usage}

@app.get("/ram")
def get_ram_usage():
    ram = psutil.virtual_memory()
    ram_usage = ram.percent  # Obtém a porcentagem de uso da RAM
    logging.info("Recuperando RAM")
    return {"ram_usage": ram_usage}

@app.get("/start")
async def start_measurement():
    # Limpa o vetor de medidas
    measurements.clear()
    logging.info("Iniciando start")
    # Realiza a coleta de medidas a cada 10 segundos por 1 minuto
    for _ in range(6):  # 6 vezes para 1 minuto
        # Simula a coleta de medidas de CPU e RAM (substitua por sua lógica real)
        cpu_measurement = get_cpu_measurement()
        ram_measurement = get_ram_measurement()

        # Armazena as medidas no vetor
        measurements.append({"cpu": cpu_measurement, "ram": ram_measurement})

        # Aguarda 10 segundos
        time.sleep(10)
    logging.info("Pausando start")
    return {"message": "Medições iniciadas"}

@app.get("/get_metrics")
async def get_measurements():
    # Retorna as medidas armazenadas
    logging.info("Recuperando metrics")
    return measurements

def get_cpu_measurement():
    return psutil.cpu_percent(interval=1)  # Obtém a porcentagem de uso da CPU

def get_ram_measurement():
    # Simulação de medida de RAM
    return psutil.virtual_memory().percents

if __name__ == "__main__":
# update uvicorn access logger format
    #log_config = uvicorn.config.LOGGING_CONFIG
    #log_config["formatters"]["access"]["fmt"] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    LoggingInstrumentor().instrument(set_logging_format=True)
    uvicorn.run(
        app,
        host=app_host,
        port=int(app_port),
        #log_config=log_config
    )