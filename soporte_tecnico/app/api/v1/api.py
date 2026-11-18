from fastapi import APIRouter
from app.api.v1.routes import categoria_routes, solicitud_routes

api_router = APIRouter()
api_router.include_router(categoria_routes.router)
api_router.include_router(solicitud_routes.router)