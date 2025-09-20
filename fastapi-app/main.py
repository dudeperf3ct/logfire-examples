"""FastAPI application."""

from contextlib import asynccontextmanager

import logfire
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from sqlmodel import Session, select

from database import get_session, init_db
from models import User
from schemas import UserCreate, UserRead

# Set logfire token
load_dotenv()

# Custom metrics
user_counter = logfire.metric_counter(
    name="users_created_total",
    description="Number of users created",
)


def setup_logfire(app: FastAPI):
    logfire.configure(send_to_logfire="if-token-present")
    logfire.instrument_pydantic(record="all")
    logfire.instrument_system_metrics()
    logfire.instrument_fastapi(app, capture_headers=True, record_send_receive=False)
    # Logs will appear only after this is set
    logger.configure(handlers=[logfire.loguru_handler()])


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    setup_logfire(app)
    with logfire.span("initialize_database"):
        logger.info("Initializing database")
        init_db()
    logger.info("FastAPI + Logfire app started")
    yield
    # Shutdown code
    logger.info("FastAPI app shutting down")


app = FastAPI(title="FastAPI + Pydantic + Logfire Demo", lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Log to Logfire
    logfire.error(
        "Validation error",
        extra={"errors": exc.errors(), "body": exc.body, "path": str(request.url)},
    )
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


@app.post("/create_users/", response_model=UserRead)
@logfire.instrument("create_user")
def create_user(user_in: UserCreate, session: Session = Depends(get_session)):
    """Create a new user and record metrics."""
    logger.info(f"Creating user {user_in.name} <{user_in.email}>")
    user = User.model_validate(user_in)
    session.add(user)
    session.commit()
    session.refresh(user)
    user_counter.add(1)
    return user


@app.get("/list_users/", response_model=list[UserRead])
@logfire.instrument("list_users")
def list_users(session: Session = Depends(get_session)):
    """List all users."""
    users = session.exec(select(User)).all()
    return users
