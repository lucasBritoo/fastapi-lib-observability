from lib_fastapi.lib_fastapi import FastApiObservability
from prometheus_client import Counter
from lib_fastapi.lib_log import Logger
from lib_fastapi.lib_instrumentation import Instrumentation
from datetime import datetime
import logging
import uvicorn
import psutil
import os

METRICS_EXPORTER_URL = os.environ.get("METRICS_EXPORTER_URL")
TRACES_EXPORTER_URL = os.environ.get("TRACES_EXPORTER_URL")
LOGS_EXPORTER_URL= os.environ.get("LOGS_EXPORTER_URL")
APP_NAME= os.environ.get("APP_NAME")
APP_HOST= os.environ.get("APP_HOST")
APP_PORT= os.environ.get("APP_PORT")
APP_VERSION= os.environ.get("APP_VERSION")
LOG_FILE = os.environ.get("LOG_FILE")

fastApiObservability= FastApiObservability(path="/", name=APP_NAME, version=APP_VERSION)
app= fastApiObservability.get_api_application()

# my_counter = Counter('meu_contador', 'Descrição do meu contador')
logger = logging.getLogger(__name__)

@app.get('/data')
def get_system_date():
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info("Recuperando Data")
    return {"date": current_date}

@app.get("/cpu")
def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    logger.info("Recuperando CPU")
    # my_counter.inc()
    return {"cpu_usage": cpu_usage}

@app.get("/ram")
def get_ram_usage():
    ram = psutil.virtual_memory()
    ram_usage = ram.percent
    logger.debug("Recuperando RAM")
    return {"ram_usage": ram_usage}

def get_cpu_measurement():
    return psutil.cpu_percent(interval=1)

def get_ram_measurement():
    return psutil.virtual_memory().percents

if __name__ == "__main__":

    logConfig = Logger(appName=APP_NAME, name=APP_NAME, level=logging.DEBUG)
    logConfig.setLogFile(path=LOG_FILE)
    # logConfig.setLogExporter(url=LOGS_EXPORTER_URL)
    logConfig.setLogConsole()
    logConfig.setFormatter()
    logConfig.setBasicConfig()
    fastApiObservability.setInstrumentorTraces(grpc=True, url=TRACES_EXPORTER_URL)
    fastApiObservability.setMetricsPrometheus()
    # fastApiObservability.setExporterPushGateway(url=METRICS_EXPORTER_URL)
    
    uvicorn.run(
        app,
        host=APP_HOST,
        port=int(APP_PORT),
        log_config=logConfig.getConfig()
    )