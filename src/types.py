from pydantic import BaseModel


class LabelPrediction(BaseModel):
    token: str
    label: str
