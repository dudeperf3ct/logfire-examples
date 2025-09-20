# LLM Application

This application consists of a single `generate` endpoint. It sends the request to LLM and return the response.

## Getting Started

Environment setup and dependecies installed using `uv`

```bash
uv init
source .venv/bin/activate
uv sync
```

Create a `.env` using `.env.example` and fill out the corresponding logfire token and OpenAI token.

Run the application using following command

```python
fastapi run main.py
```
