from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading

from app.core.config import settings
from app.routes import dashboard, vehicles, shipments, route, costs, system
from app.core.listeners.etl_listener import ETLListener
from app.utils.logger import get_logger


app = FastAPI(
    title="Logistics Analytics API",
    description="API for logistics analytics dashboard",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logger = get_logger(__name__)


# Global listener instance
@app.on_event("startup")
async def startup_event():
    global etl_listener, listener_thread

    # Initialize and start listener in a separate thread
    etl_listener = ETLListener()
    listener_thread = threading.Thread(
        target=etl_listener.start_listening,
        daemon=True,  # This ensures the thread stops when the main process stops
    )
    listener_thread.start()

    logger.info("ETL listener started")


@app.on_event("shutdown")
async def shutdown_event():
    global etl_listener
    if etl_listener:
        etl_listener.cleanup()
        logger.info("ETL listener stopped")


# Include routers
app.include_router(dashboard.router)
app.include_router(vehicles.router)
app.include_router(shipments.router)
app.include_router(route.router)
app.include_router(costs.router)
app.include_router(system.router)
