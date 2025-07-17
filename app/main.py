#create fastapi app calling the lina_router
from fastapi import FastAPI
from app.routers.lina_router import router as lina_router

def create_app():
    app = FastAPI(
        title="LINA Application", 
        description="API for LINA Application",
        version="1.0")

    app.include_router(lina_router)

    return app

app = create_app()

