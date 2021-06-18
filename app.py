import logging
from flask import Flask, request

from opentelemetry import propagators, trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

FlaskInstrumentor().instrument_app(app)

tracer_provider = TracerProvider(resource=Resource.create({"service.name": "backend"}))
tracer_provider.add_span_processor(
    SimpleSpanProcessor(OTLPSpanExporter(endpoint="localhost:55680"))
)
trace.set_tracer_provider(tracer_provider)

@app.route("/backend")
def server_request():
    return "served"
    
@app.route("/testing")
def server_request1():
    return "app testing"
    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081)
