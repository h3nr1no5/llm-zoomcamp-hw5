from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

""" provider = TracerProvider()
provider.add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("llm-zoomcamp")
 """
from starter import rag


# with tracer.start_as_current_span("my_operation") as span:
    # your code here
query = "How does the agentic loop keep calling the model until it stops?"
response = rag.rag(query)
answer = response.output_text
usage = response.usage
print(answer)

    # span.set_attribute("input_tokens", usage.input_tokens)
    # span.set_attribute("output_tokens", usage.output_tokens)

