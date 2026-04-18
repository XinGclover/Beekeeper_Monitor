from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from api.routers.monitoring_sensors import router as monitoring_sensors_router
from api.routers.monitoring_weather import router as monitoring_weather_router
from api.routers.monitoring_wildfire import router as monitoring_wildfire_router
from api.routers.monitoring_locations import router as monitoring_locations_router
from api.routers.monitoring_alarms import router as monitoring_alarms_router
from api.routers.monitoring_notifications import router as monitoring_notifications_router

app = FastAPI(title="Beekeeper Monitoring API")

app.include_router(monitoring_sensors_router)
app.include_router(monitoring_weather_router)
app.include_router(monitoring_wildfire_router)
app.include_router(monitoring_locations_router)
app.include_router(monitoring_alarms_router)
app.include_router(monitoring_notifications_router)

@app.get("/")
def root():
    return {"message": "Beekeeper Monitoring API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}