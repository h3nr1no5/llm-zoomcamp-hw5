import time

from rag_helper import RAGBase

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor



class RAGTraced(RAGBase):
    def __init__(self, index, llm_client, **kwargs):
        self.input_tokens = 0
        provider = TracerProvider()
        provider.add_span_processor(
            SimpleSpanProcessor(ConsoleSpanExporter())
        )
        trace.set_tracer_provider(provider)

        self.tracer = trace.get_tracer("llm-zoomcamp")
        super().__init__(index, llm_client, **kwargs)

    def search(self, query, num_results=5):
        with self.tracer.start_as_current_span("search") as span:
            start_ns = time.time_ns()
            search_results = super().search(query, num_results)
            duration_ms = (time.time_ns() - start_ns) / 1e6
            span.set_attribute("duration_ms", round(duration_ms, 2))
        return search_results


    def llm(self, prompt):
        with self.tracer.start_as_current_span("llm") as span:
            start_ns = time.time_ns()
            response = super().llm(prompt)
            if hasattr(response, 'usage'):
                usage = response.usage
                span.set_attribute("input_tokens", usage.input_tokens)
                span.set_attribute("output_tokens", usage.output_tokens)
                self.input_tokens = usage.input_tokens
                
            duration_ms = (time.time_ns() - start_ns) / 1e6
            span.set_attribute("duration_ms", round(duration_ms, 2))
        return response


    def rag(self, query):
        with self.tracer.start_as_current_span("rag") as span:
            start_ns = time.time_ns()
            response = super().rag(query)
            duration_ms = (time.time_ns() - start_ns) / 1e6
            span.set_attribute("duration_ms", round(duration_ms, 2))
            return response

    def input_tokens(self):
        return self.input_tokens