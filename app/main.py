"""FastAPI application entry point."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.tasks import router as tasks_router

# Which browser origins may call this API.
# Overridable with an env var so Docker/Compose can change it without a rebuild.
default_origins = "http://localhost:5173,http://localhost:3000"
allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", default_origins).split(",")
    if origin.strip()
]

app = FastAPI(
    title="Task Manager API",
    description="A tiny in-memory task API used for learning Docker.",
    version="1.0.0",
)

# CORS: the React dev server runs on port 5173 and the API on 8000.
# Different port = different origin, so the browser blocks the request
# unless the API explicitly allows that origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(tasks_router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Liveness check. Docker and Compose use this to know the API is up."""
    return {"status": "ok"}


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"message": "Task Manager API. See /docs for the interactive docs."}
