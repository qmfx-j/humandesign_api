from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class VariableDetail(BaseModel):
    value: str
    name: str
    aspect: str
    def_type: str

class Variables(BaseModel):
    top_right: VariableDetail
    bottom_right: VariableDetail
    top_left: VariableDetail
    bottom_left: VariableDetail

class GeneralOutput(BaseModel):
    birth_date: str
    create_date: str
    birth_place: Optional[str] = None
    energy_type: str
    inner_authority: str
    inc_cross: str
    profile: str
    active_chakras: List[str]
    inactive_chakras: List[str]
    definition: str
    variables: Variables
    age: Optional[int] = Field(None, description="Calculated age in years")
    zodiac_sign: Optional[str] = Field(None, description="Western astrological sign")
    gender: Optional[str] = "male"
    islive: Optional[bool] = Field(True, description="Whether the person is still alive (True) or deceased (False)")

class GateInfo(BaseModel):
    gate: int
    line: int
    color: int
    tone: int
    base: int
    is_active: bool

class ChannelInfo(BaseModel):
    name: str
    gates: List[int]
    meaning: Optional[str] = None

class CalculateResponse(BaseModel):
    general: GeneralOutput
    channels: List[ChannelInfo]
    gates: Dict[str, List[GateInfo]]
