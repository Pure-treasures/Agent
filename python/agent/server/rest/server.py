import uvicorn

from ..settings import Settings
from ..handlers import DataPlane

from .app import create_app
from .logging import get_logger
from typing import Optional

logger = get_logger()

class _NoSignalServer(uvicorn.Server):
    def install_signal_handlers(self):
        pass

class RESTServer:
    def __init__(
        self,
        settings: Settings,
        data_plane: DataPlane
    ):
        self._settings = settings
        self._data_plane = data_plane
        self._app = create_app(
            data_plane=self._data_plane
        )

    async def start(self):
        cfg = self._get_config()
        self._server = _NoSignalServer(cfg)

        await self._server.serve()

    def _get_config(self):
        kwargs = {}

        kwargs.update(
            {
                "host": self._settings.host,
                "port": self._settings.http_port,
                # "root_path": self._settings.root_path,
            }
        )

        return uvicorn.Config(self._app, **kwargs)

    async def stop(self, sig: Optional[int] = None):
        self._server.handle_exit(sig=sig, frame=None)