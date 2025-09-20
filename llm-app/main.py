"""FastAPI application with Logfire + LiteLLM."""

from contextlib import asynccontextmanager

import logfire
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from loguru import logger

from llm_utils import generate
from schemas import LLMRequest, LLMResponse

# Load env vars
load_dotenv()


def setup_logfire(app: FastAPI):
    logfire.configure(send_to_logfire="if-token-present")
    logfire.instrument_system_metrics()
    logfire.instrument_fastapi(app)
    logfire.instrument_litellm()
    logfire.instrument_pydantic("failure")
    logger.configure(handlers=[logfire.loguru_handler()])


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logfire(app)
    logger.info("FastAPI + LLM app started")
    yield
    logger.info("FastAPI + LLM app shutting down")


app = FastAPI(title="FastAPI + LiteLLM + Logfire Demo", lifespan=lifespan)


@app.post("/generate/", response_model=LLMResponse)
@logfire.instrument("generate_text")
async def generate_text(request: LLMRequest):
    """Generate text using an LLM."""
    try:
        result = await generate(
            prompt=request.prompt,
            model=request.model or "gpt-4o-mini",
            temperature=request.temperature or 0.0,
        )
        logger.info(f"LLM response: {result['text']}")
        logger.info(f"Token usage: {result['tokens']}")
        return LLMResponse(
            text=result["text"],
            model=request.model or "gpt-4o-mini",
            duration=result["duration"],
            tokens=result["tokens"],
        )
    except Exception as e:
        logger.exception("Error in generate_text endpoint")
        raise HTTPException(status_code=500, detail=str(e))
