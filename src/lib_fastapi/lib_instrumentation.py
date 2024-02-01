from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace
from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)

class Instrumentation():

    def setting_otlp(self,app: FastAPI = None, appName: str = "app", url = "http://localhost:4317") -> None:
        resource = Resource.create(attributes={
            "service.name": appName,
            "compose_service": appName
        })


        logger.debug("teste")
        tracer = TracerProvider(resource=resource)
        tracer.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=url)))
        trace.set_tracer_provider(tracer)
        FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)