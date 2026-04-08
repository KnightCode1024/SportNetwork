from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sport_network_api.ioc import async_setup_dishka
from sport_network_api.controllers import root_controller
from sport_network_api.infrastructure.taskiq_broker import broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.startup()
    yield
    await broker.shutdown()

def create_fastapi_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    async_setup_dishka(app=app)
    app.include_router(root_controller)
    return app

app = create_fastapi_app()

@app.get("/ping")
def ping():
    return {"message": "pong"}
