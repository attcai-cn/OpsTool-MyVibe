from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Literal
from app.utils.calculator import convert_bandwidth, convert_timestamp, calculate_subnet

router = APIRouter(prefix="/calculator", tags=["Calculator"])


def make_response(code: int = 200, message: str = "ok", data=None):
    return {"code": code, "message": message, "data": data}


class BandwidthRequest(BaseModel):
    value: float = Field(..., gt=0)
    from_unit: Literal["bps", "Bps", "Kbps", "KBps", "Mbps", "MBps", "Gbps", "GBps"]
    to_unit: Literal["bps", "Bps", "Kbps", "KBps", "Mbps", "MBps", "Gbps", "GBps"]


@router.post("/bandwidth", response_model=dict)
def bandwidth(req: BandwidthRequest):
    result = convert_bandwidth(req.value, req.from_unit, req.to_unit)
    return make_response(
        data={
            "value": req.value,
            "from": req.from_unit,
            "to": req.to_unit,
            "result": round(result, 6),
        }
    )


class TimestampRequest(BaseModel):
    timestamp: int | None = None
    datetime_str: str | None = Field(default=None, alias="datetime")


@router.post("/timestamp", response_model=dict)
def timestamp(req: TimestampRequest):
    data = convert_timestamp(
        timestamp=req.timestamp,
        dt_str=req.datetime_str,
    )
    return make_response(data=data)


class SubnetRequest(BaseModel):
    cidr: str = Field(..., pattern=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$")


@router.post("/subnet", response_model=dict)
def subnet(req: SubnetRequest):
    data = calculate_subnet(req.cidr)
    return make_response(data=data)
