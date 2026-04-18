from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import router

app = FastAPI(
    title="Previsão do Clima",
    description="Web app de clima com mapa de chuva interativo",
    version="2.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)
