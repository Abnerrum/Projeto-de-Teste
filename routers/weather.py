from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import asyncio

from services import geocode, fetch_weather, fetch_rain_regions, build_context

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/weather", response_class=HTMLResponse)
async def weather(request: Request, city: str = ""):
    city = city.strip()
    if not city:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Digite o nome de uma cidade."
        })

    geo = await geocode(city)
    if not geo:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Cidade '{city}' não encontrada. Tente outro nome.",
            "query": city,
        })

    # fetch weather + rain regions concurrently
    raw, regions = await asyncio.gather(
        fetch_weather(geo["lat"], geo["lon"]),
        fetch_rain_regions(geo["lat"], geo["lon"]),
    )

    ctx = build_context(geo, raw, regions)
    ctx["request"] = request
    ctx["query"]   = city
    return templates.TemplateResponse("index.html", ctx)


@router.get("/api/weather")
async def api_weather(city: str = ""):
    """JSON endpoint for programmatic access."""
    city = city.strip()
    if not city:
        return JSONResponse({"error": "city param required"}, status_code=400)

    geo = await geocode(city)
    if not geo:
        return JSONResponse({"error": "city not found"}, status_code=404)

    raw, regions = await asyncio.gather(
        fetch_weather(geo["lat"], geo["lon"]),
        fetch_rain_regions(geo["lat"], geo["lon"]),
    )

    ctx = build_context(geo, raw, regions)
    return JSONResponse(ctx)
