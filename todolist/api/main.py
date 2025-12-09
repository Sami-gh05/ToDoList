from __future__ import annotations

from fastapi import FastAPI

from todolist.api.router import api_router
from todolist.config.settings import Settings


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    Settings.load()  # ensure env is loaded
    app = FastAPI(
        title="ToDoList API",
        version="0.3.0",
        description="Phase 3 REST API for ToDoList",
    )

    @app.get("/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(api_router)
    return app


app = create_app()


def run() -> None:
    """Run a development server with uvicorn."""
    import uvicorn

    uvicorn.run("todolist.api.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run()

