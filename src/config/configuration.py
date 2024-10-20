import os
from typing import Optional

from pydantic import BaseModel


class Configuration(BaseModel):
    HF_MODEL_NAME: str = os.getenv("HF_MODEL_NAME", "ss108/legal-citation-bert")

    MODEL_URL: Optional[str] = os.getenv("MODEL_URL")
