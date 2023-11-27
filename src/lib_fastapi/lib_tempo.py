from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry import trace

class InstrumentationTempo():
    def __init__(self, app, name="app", tempoUrl="tempo:3000"):
        self.app = app
        self.name = name
        self.tempoUrl = tempoUrl

        self.setting_otlp(False)


    def setting_otlp(self, log_correlation: bool = True) -> None:
        resource = Resource.create(attributes={
            "service.name": self.name,
            "compose_service": self.name
        })


        tracer = TracerProvider(resource=resource)
        trace.set_tracer_provider(tracer)

        tracer.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=self.tempoUrl)))

        if log_correlation:
            LoggingInstrumentor().instrument(set_logging_format=True)
            
        FastAPIInstrumentor.instrument_app(self.app, tracer_provider=tracer)