import time
import datetime
import threading
import schedule
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client.openmetrics.exposition import (CONTENT_TYPE_LATEST,
                                                      generate_latest)
from starlette.responses import Response
from prometheus_client import REGISTRY, pushadd_to_gateway

from lib_fastapi.lib_prometheus import PrometheusMiddleware
from lib_fastapi.lib_tempo import InstrumentationTempo


class FastApiObservability:

    def __init__(self, path="", name="app", version="0.0.1", prometheus=None, pushGateway=None,
                 pushGatewayUrl=None,tempo=None, tempoUrl=None):
        self.pushGatewayUrl = pushGatewayUrl
        self.tempoUrl = tempoUrl
        self.name = name
        
        self.app = FastAPI(
            title=name,
            version=version,
            docs_url=f"{path}/docs/",
            openapi_url="/openapi.json"
        )

        self.app.router.redirect_slashes = False

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        if prometheus or pushGateway:
            self.app.add_middleware(PrometheusMiddleware, app_name=name)

        if prometheus:
            self.app.add_route("/metrics", self.metrics)
            
        if pushGateway: 
            schedule.every(10).seconds.do(self.send_metrics)
            metrics_thread = threading.Thread(target=self.send_metrics_timer)
            metrics_thread.daemon = True
            metrics_thread.start()

        if tempo:
            InstrumentationTempo(self.app, self.name, self.tempoUrl)

        @self.app.middleware("http")
        async def add_process_time_header(request: Request, call_next):
            start_time = time.time()
            response = await call_next(request)
            response.headers['response_time'] = str(
                datetime.timedelta(seconds=(time.time() - start_time))
            )
            return response
        
    def get_api_application(self):
        return self.app

    def metrics(self, request: Request) -> Response:
        return Response(generate_latest(REGISTRY), headers={"Content-Type": CONTENT_TYPE_LATEST})
    
    def send_metrics(self):
        try:
            logging.info("Metrics sending to pushGateway")
            pushadd_to_gateway(self.pushGatewayUrl, job=self.name, registry=REGISTRY)
        except Exception as e:
            logging.error(f"Error send metrics to pushGateway: {e}")
            
    def send_metrics_timer(self):
        while True:
            schedule.run_pending()
            time.sleep(1)