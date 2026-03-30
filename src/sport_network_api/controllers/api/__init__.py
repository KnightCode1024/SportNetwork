from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute

from .v1 import v1_controller

root_controller = APIRouter(prefix="", route_class=DishkaRoute)

controllers = [
    v1_controller,
]

for controller in controllers:
    root_controller.include_router(controller)


__all__ = [
    "root_controller",
]
