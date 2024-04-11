from typing import Callable
from fastapi import FastAPI
from fastapi.responses import Response as FastAPIResponse
from fastapi.routing import APIRoute as FastAPIRoute

from .endpoints import Endpoints
from .requests import Request
from .responses import Response
from .errors import _EXCEPTION_HANDLERS
from ..handlers import DataPlane

class APIRoute(FastAPIRoute):
    """
    Custom route to use our own Request handler.
    """

    def __init__(
        self,
        *args,
        response_model_exclude_unset=True,
        response_model_exclude_none=True,
        response_class=Response,
        **kwargs
    ):
        super().__init__(
            *args,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_none=response_model_exclude_none,
            response_class=response_class,
            **kwargs
        )

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> FastAPIResponse:
            request = Request(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler

def create_app(
    data_plane: DataPlane,
) -> FastAPI:
    endpoints = Endpoints(data_plane)
    
    routes = [
        APIRoute(
            "/api/v2/add_report",
            endpoints.add_document,
            methods=["POST"],
            tags=["document-qa"]
        ),
    ]
    
    app = FastAPI(
        routes=routes,  # type: ignore
        default_response_class=Response,
        exception_handlers=_EXCEPTION_HANDLERS,  # type: ignore
    )
    app.router.route_class = APIRoute
    
    return app