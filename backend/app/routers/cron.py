from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Literal
from app.utils.cron import (
    build_cron_expression,
    get_next_executions,
    parse_cron_expression,
)

router = APIRouter(prefix="/cron", tags=["Cron"])


def make_response(code: int = 200, message: str = "ok", data=None):
    return {"code": code, "message": message, "data": data}


class CronBuildRequest(BaseModel):
    mode: Literal["daily", "weekly"] = Field(..., description="daily=每天, weekly=每周")
    minute: int = Field(default=0, ge=0, le=59)
    hour: int = Field(default=0, ge=0, le=23)
    day_of_week: int | None = Field(
        default=None, ge=0, le=6, description="0=周日, 1=周一, ..., 6=周六"
    )


@router.post("/build", response_model=dict)
def build_cron(req: CronBuildRequest):
    if req.mode == "weekly" and req.day_of_week is None:
        return make_response(code=400, message="weekly mode requires day_of_week")

    cron_expr = build_cron_expression(
        minute=req.minute,
        hour=req.hour,
        day_of_week=req.day_of_week if req.mode == "weekly" else None,
    )

    next_times = get_next_executions(cron_expr, count=5)
    parsed = parse_cron_expression(cron_expr)

    return make_response(
        data={
            "expression": cron_expr,
            "description": parsed["description"],
            "next_executions": next_times,
        }
    )


class CronParseRequest(BaseModel):
    expression: str = Field(..., min_length=1, description="5-field cron expression")


@router.post("/parse", response_model=dict)
def parse_cron(req: CronParseRequest):
    try:
        parsed = parse_cron_expression(req.expression)
        next_times = get_next_executions(req.expression, count=5)
        return make_response(
            data={
                **parsed,
                "next_executions": next_times,
            }
        )
    except ValueError as e:
        return make_response(code=400, message=str(e))
