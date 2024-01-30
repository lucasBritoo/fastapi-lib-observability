import psutil
from datetime import datetime
import time

import logging
import os
import time

import uvicorn

from lib_fastapi.lib_fastapi import FastApiObservability
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from prometheus_client import REGISTRY, Counter
from lib_fastapi.lib_log import Logger

push_gateway_host = os.environ.get("PUSH_GATEWAY_HOST")
push_gateway_port = os.environ.get("PUSH_GATEWAY_PORT")
app_name= os.environ.get("APP_NAME")
app_host= os.environ.get("APP_HOST")
app_port= os.environ.get("APP_PORT")
app_version= os.environ.get("APP_VERSION")
tempo_port= os.environ.get("TEMPO_PORT")
tempo_host= os.environ.get("TEMPO_HOST")

push_gateway_url = 'http://' + push_gateway_host + ":" + push_gateway_port
tempo_url = 'http://' + tempo_host + ':' + tempo_port + '/v1/traces'

print(app_name)

# app = FastApiObservability(path="/", name=app_name, version=app_version,
#                            prometheus=True, tempo=True, tempoUrl=tempo_url).get_api_application()

app = FastApiObservability(path="/", name=app_name, version=app_version, tempo=True, tempoUrl=tempo_url).get_api_application()

REQUEST_TESTE = Counter(
    "fastapi_requests_teste", "Total count of requests by method and path.",  ["app_name"]
)

# Vetor para armazenar as medidas
measurements = []

logger = Logger(__name__, logging.DEBUG).getLogger()


@app.get('/data')
def get_system_date():
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info("Recuperando Data")
    return {"date": current_date}

@app.get("/cpu")
def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)  # Obtém a porcentagem de uso da CPU
    logger.info("Recuperando CPU")
    # REQUEST_TESTE.labels(app_name=app_name).inc()
    return {"cpu_usage": cpu_usage}

@app.get("/ram")
def get_ram_usage():
    ram = psutil.virtual_memory()
    ram_usage = ram.percent  # Obtém a porcentagem de uso da RAM
    logger.info("Recuperando RAM")
    return {"ram_usage": ram_usage}

@app.get("/start")
async def start_measurement():
    # Limpa o vetor de medidas
    measurements.clear()
    logger.info("Iniciando start")
    # Realiza a coleta de medidas a cada 10 segundos por 1 minuto
    for _ in range(6):  # 6 vezes para 1 minuto
        # Simula a coleta de medidas de CPU e RAM (substitua por sua lógica real)
        cpu_measurement = get_cpu_measurement()
        ram_measurement = get_ram_measurement()

        # Armazena as medidas no vetor
        measurements.append({"cpu": cpu_measurement, "ram": ram_measurement})

        # Aguarda 10 segundos
        time.sleep(10)
    logger.info("Pausando start")
    return {"message": "Medições iniciadas"}

@app.get("/get_metrics")
async def get_measurements():
    # Retorna as medidas armazenadas
    logger.info("Recuperando metrics")
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
    # LoggingInstrumentor().instrument(set_logging_format=True)
    uvicorn.run(
        app,
        host=app_host,
        port=int(app_port),
        #log_config=log_config
    )