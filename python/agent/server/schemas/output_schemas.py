from pydantic import BaseModel as _BaseModel, Field
from typing import Dict, List, Any, Optional

class BaseModel(_BaseModel):
    class Config:
        extra = 'ignore'
        