import os
from pathlib import Path
from typing import List
from fastapi import UploadFile

from ..settings import Settings
from ..schemas import output_schemas
from ..utils.logging import get_logger
from ..utils import dataplane_utils

logger = get_logger(__name__)

class DataPlane(object):
    """
    Internal implementation of handlers, used by REST servers.
    """

    def __init__(self, settings: Settings):
        self._settings = settings
        # Load the env
        from dotenv import load_dotenv
        load_dotenv()
        
      