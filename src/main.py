from lib_fastapi.lib_fastapi import FastApiObservability
from lib_fastapi.lib_log import Logger
from lib_fastapi.lib_instrumentation import Instrumentation
from datetime import datetime
import logging
import uvicorn
import psutil
import os


push_gateway_host = os.environ.get("PUSH_GATEWAY_HOST")
push_gateway_port = os.environ.get("PUSH_GATEWAY_PORT")
app_name= os.environ.get("SERVICE_NAME")
app_host= os.environ.get("APP_HOST")
app_port= os.environ.get("APP_PORT")
app_version= os.environ.get("APP_VERSION")
tempo_port= os.environ.get("TEMPO_PORT")
tempo_host= os.environ.get("TEMPO_HOST")
log_file = os.environ.get("LOG_FILE")

push_gateway_url = 'http://' + push_gateway_host + ":" + push_gateway_port
tempo_url = 'http://' + tempo_host + ':' + tempo_port + '/v1/traces'

app = FastApiObservability(path="/", name=app_name, version=app_version).get_api_application()

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

    logConfig = Logger(appName=app_name, name=app_name, level=logging.DEBUG)
    # logConfig.setLogFile(path=log_file)
    logConfig.setLogExporter(url="http://otel-collector:4317")
    logConfig.setLogConsole()
    logConfig.setFormatter()
    logConfig.setBasicConfig()
    # Instrumentation().setting_otlp(app=app, appName=app_name, grpc=True, url="http://otel-collector:4317")
    Instrumentation().setting_otlp(app=app, appName=app_name, grpc=True, url="http://tempo:8004/v1/traces")

    uvicorn.run(
        app,
        host=app_host,
        port=int(app_port),
        log_config=logConfig.getConfig()
    )