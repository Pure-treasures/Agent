from .settings import Settings
from .server import QAServer
from .utils.logging import get_logger
import asyncio

logger = get_logger()
async def main():
    settings = Settings(
        http_port=6008
    )
    logger.info(f"The parameters of the qa-server: \n{settings.__str__()}")
    
    server = QAServer(settings)
    await server.start()

if __name__=="__main__":
    asyncio.run(main())