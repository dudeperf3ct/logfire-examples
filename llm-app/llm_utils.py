"""LLM utils."""

import time

import logfire
from litellm import acompletion
from loguru import logger

from metrics import (
    llm_error_counter,
    llm_latency_histogram,
    llm_request_counter,
    llm_tokens_counter,
)


async def generate(
    prompt: str, model: str = "gpt-4o-mini", temperature: float = 0.0
) -> dict:
    with logfire.span("llm.call"):
        start = time.perf_counter()
        try:
            response = await acompletion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            duration = time.perf_counter() - start

            # Metrics
            llm_request_counter.add(1, {"model": model})
            llm_latency_histogram.record(duration, {"model": model})

            # Extract tokens if available
            tokens = None
            usage = getattr(response, "usage", None)
            if usage:
                tokens = usage.get("total_tokens")
                if tokens:
                    llm_tokens_counter.add(tokens, {"model": model})

            # Extract text
            text = ""
            if response.choices and len(response.choices) > 0:
                text = response.choices[0].message["content"]

            logger.info(
                "LLM call succeeded",
                extra={"model": model, "duration_s": duration, "tokens": tokens},
            )

            return {
                "raw": response,
                "text": text,
                "duration": duration,
                "tokens": tokens,
            }

        except Exception:
            llm_error_counter.add(1, {"model": model})
            logger.exception("LLM call failed")
            raise
