import uvicorn
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.apis import api_router
from app.core import (
    create_tables_async,
    check_db_connection,
    close_db_connections,
    settings,
)
from app.core.utils.response import BaseResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print(f"{settings.app_name} v{settings.app_version} starting up...")

        if not settings.validate_database_config():
            print("Configuration validation failed. Cannot start application.")
            raise RuntimeError("Invalid configuration")

        if await check_db_connection():
            print("Database connection established")

            await create_tables_async()
            print("Database tables created/verified successfully")
        else:
            print("Database connection failed")
            raise RuntimeError("Database connection failed")

        if settings.debug:
            print(f"Debug mode: {settings.debug}")
            print(f"Database URL: {settings.database_url}")

    except Exception as e:
        print(f"Error during startup: {e}")
        raise e

    yield

    try:
        print("Shutting down Legal Lingo API...")
        await close_db_connections()
        print("Database connections closed")
    except Exception as e:
        print(f"Error during shutdown: {e}")


if settings is None:
    print("Failed to load configuration. Exiting...")
    sys.exit(1)

app = FastAPI(
    title=settings.app_name,
    description="A comprehensive API for Legal Lingo",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.debug,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins
    if hasattr(settings, "allowed_origins")
    else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)


@app.get("/")
async def root():
    return BaseResponse.success(
        message=f"Welcome to {settings.app_name}",
        data={
            "app_name": settings.app_name,
            "version": settings.app_version,
            "endpoints": {
                "swagger": "/docs",
                "redoc": "/redoc",
                "health": f"{settings.api_prefix}/health",
            },
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=10000,
        reload=settings.debug,
        log_level="info",
    )
