from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.logging import LoggingInstrumentor
import logging
import os

class EndpointFilter(logging.Filter):

    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find('GET /metrics') == -1

class Logger():
    
    def __init__(self, name, level):
        
        self.logger = logging.getLogger(name)
        self.logger.addFilter(EndpointFilter())
        self.logger.setLevel(level)
        # logger.addHandler(handler)
    
    def getLogger(self):
        return self.logger

# logger_provider = LoggerProvider(
#     resource=Resource.create(
#         {
#             "service.name": "train-the-telemetry",
#             "service.instance.id": os.uname().nodename,
#         }
#     ),
# )
# set_logger_provider(logger_provider)

# otlp_exporter = OTLPLogExporter(endpoint="http://otel-collector:4317", insecure=True)
# logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_exporter))
# handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

