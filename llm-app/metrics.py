"""Custom logfire metrics."""

import logfire

llm_request_counter = logfire.metric_counter(
    name="llm_requests_total",
    description="Number of LLM requests made",
)

llm_latency_histogram = logfire.metric_histogram(
    name="llm_request_duration_seconds",
    description="Duration of LLM requests",
    unit="s",
)

llm_tokens_counter = logfire.metric_counter(
    name="llm_tokens_total",
    description="Total LLM tokens consumed",
)

llm_error_counter = logfire.metric_counter(
    name="llm_requests_failed_total",
    description="Failed LLM requests",
)
