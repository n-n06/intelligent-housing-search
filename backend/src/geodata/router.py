from fastapi.routing import APIRouter

from src.geodata.parser import main
from src.geodata.test import test_get_info
from src.config import settings


geo_router = APIRouter(prefix="/geo", tags=["Geodata"])

@geo_router.get("/")
async def get_geodata():
    return await main()


test_router = APIRouter(prefix="/test", tags=["Test"])

@test_router.get("/test-ardak")
async def get_ardak_info():
    return await test_get_info(address=settings.ARDAK_ADDRESS)

@test_router.get("/test-anele")
async def get_anele_info():
    return await test_get_info(address=settings.ANELE_ADDRESS)
