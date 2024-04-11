from typing import List
from fastapi import Body, UploadFile, Form

from ..handlers import DataPlane
from ..schemas import input_schemas


class Endpoints(object):
    """
    Implementation of REST endpoints.
    These take care of the REST/HTTP-specific things and then delegate the
    business logic to the internal handlers.
    """
    def __init__(self, data_plane: DataPlane):
        self._data_plane = data_plane
    