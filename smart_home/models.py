from pydantic import BaseModel
from typing_extensions import Literal


class ItemCreation(BaseModel):
    name: str
    kind: Literal["Light", "PushButton", "Blind"]
    pin: str


class Item(BaseModel):
    id: int
    name: str
    kind: str
    pin: str


class RuleCreation(BaseModel):
    name: str
    kind: str
    trigger: str
    items: list


class LightDto(BaseModel):
    name: str
    on: bool
    pin: str


class LightAction(BaseModel):
    switch: bool
