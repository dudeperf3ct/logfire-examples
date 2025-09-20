import random
import time

import httpx
import logfire
from dotenv import load_dotenv
from loguru import logger

# Get logfire token
load_dotenv()

# Define a counter and histogram for tracking metrics
task_counter = logfire.metric_counter(
    name="tasks_processed_total",
    description="Number of tasks processed",
)

task_duration = logfire.metric_histogram(
    name="task_duration_seconds",
    description="Duration of each processed task",
    unit="s",
)


def setup_logfire():
    """Authenticate with logfire."""
    logfire.configure(send_to_logfire="if-token-present")
    # basic system metrics such as cpu and memory
    # there is "full" metrics that can be expensive
    # as it collects a lot other metrics in addition to cpu and memory
    logfire.instrument_system_metrics()
    # Trace all httpx requests
    logfire.instrument_httpx(capture_request_body=True, capture_response_body=True)


def setup_logger():
    """Setup logfire to act as sink for loguru logging."""
    logger.configure(handlers=[logfire.loguru_handler()])


@logfire.instrument("process_data")
def process_data(n: int) -> int:
    """Simulate a CPU-heavy calculation with tracing + metrics."""
    logger.info(f"Processing data for n={n}")
    time.sleep(random.uniform(0.2, 0.6))  # simulate work
    if n % 5 == 0:
        logger.warning("Special case encountered!")  # show log event
    result = sum(i * i for i in range(n))
    logger.info(f"Finished processing n={n}, result={result}")
    return result


@logfire.instrument("process_task")
def process_task(task_id: int):
    """Simulate work and record custom metrics."""
    start = time.perf_counter()
    logger.info(f"Starting task {task_id}")

    # Simulate variable work duration
    duration = random.uniform(0.1, 0.8)
    time.sleep(duration)

    # Record metrics
    task_counter.add(1, {"task_id": str(task_id % 3)})  # tag with group
    task_duration.record(duration, {"task_type": "simulated"})

    logger.info(f"Finished task {task_id} in {duration:.2f}s")
    return duration


@logfire.instrument("fetch_data")
def fetch_data(url: str) -> str:
    """Make an outbound HTTP request with observability."""
    logger.info(f"Fetching URL: {url}")
    try:
        response = httpx.get(url, timeout=5.0)
        response.raise_for_status()
        logger.info(f"Success: {url} -> {len(response.text)} bytes")
        return response.text
    except Exception as e:
        logger.error(f"Request failed: {e}")
        raise


if __name__ == "__main__":
    setup_logfire()
    setup_logger()
    # Run a few simulated workloads
    for i in range(1, 6):
        process_data(i)

    for i in range(1, 6):
        process_task(i)

    # Fetch some test URLs
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/status/404",
    ]
    for url in urls:
        try:
            fetch_data(url)
        except Exception:
            pass  # errors are logged & traced already
