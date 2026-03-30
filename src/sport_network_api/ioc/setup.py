from dishka.integrations.fastapi import setup_dishka
from dishka import make_async_container
from fastapi import FastAPI

from .providers import providers

def async_setup_dishka(app: FastAPI) -> None:
    async_container = make_async_container(*providers)
    setup_dishka(container=async_container, app=app)
