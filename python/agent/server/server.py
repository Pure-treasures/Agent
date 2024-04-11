import asyncio
import signal
import logging

from typing import Optional, List

from .settings import Settings
from .handlers import DataPlane
from .rest import RESTServer
from .utils.logging import get_logger

#HANDLED_SIGNALS = [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT]

logger = get_logger()

class QAServer:
    def __init__(self, settings: Settings):
        self._settings = settings
        # 此处在windows系统下会出现错误, linux系统正常
        # self._add_signal_handlers()

        self._data_plane = DataPlane(
            settings=self._settings
        )

        self._create_servers()

    def _create_servers(self):
        self._rest_server = RESTServer(
            self._settings, self._data_plane
        )

    async def start(self):
        servers = [self._rest_server.start()]
        servers_task = asyncio.gather(*servers)
        await servers_task

    # def _add_signal_handlers(self):
    #     loop = asyncio.get_event_loop()

    #     for sig in HANDLED_SIGNALS:
    #         loop.add_signal_handler(
    #             sig, lambda s=sig: asyncio.create_task(self.stop(sig=s))
    #         )

    async def stop(self, sig: Optional[int] = None):
        if self._rest_server:
            await self._rest_server.stop(sig)