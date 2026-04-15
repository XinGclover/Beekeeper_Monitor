from fastapi import FastAPI
from api.routers.monitoring_sensors import router as monitoring_sensors_router

app = FastAPI(title="Beekeeper Monitoring API")

app.include_router(monitoring_sensors_router)