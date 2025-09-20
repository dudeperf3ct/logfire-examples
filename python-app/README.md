# Application

This application consists of 3 functions: `process_task`, `process_data` and `fetch_data`.

## Getting Started

Environment setup and dependecies installed using `uv`

```bash
uv init
source .venv/bin/activate
uv sync
```

Create a `.env` using `.env.example` and fill out the corresponding logfire token to start sending the logs and traces to the logfire platform.

Run the application using following command

```python
python main.py
```
