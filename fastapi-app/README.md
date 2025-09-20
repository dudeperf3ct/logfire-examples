# LLM Application

This application consists of two endpoints : `create_user` and `list_users`. It stores and retrives data using `.db` file locally.

## Getting Started

Environment setup and dependecies installed using `uv`

```bash
uv init
source .venv/bin/activate
uv sync
```

Create a `.env` using `.env.example` and fill out the corresponding logfire token.

Run the application using following command

```python
fastapi run main.py
```
