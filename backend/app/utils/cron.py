from croniter import croniter
from datetime import datetime, timezone


def build_cron_expression(
    minute: int, hour: int, day_of_week: int | None = None
) -> str:
    """根据用户选择生成 Cron 表达式"""
    if day_of_week is None:
        # 每天
        return f"{minute} {hour} * * *"
    else:
        # 每周指定某天
        return f"{minute} {hour} * * {day_of_week}"


def get_next_executions(cron_expr: str, count: int = 5) -> list[str]:
    """获取最近 count 次执行时间"""
    try:
        itr = croniter(cron_expr, datetime.now(timezone.utc))
        times = []
        for _ in range(count):
            dt = itr.get_next(datetime)
            # 转换为本地时间字符串
            times.append(dt.astimezone().strftime("%Y-%m-%d %H:%M:%S"))
        return times
    except Exception as e:
        raise ValueError(f"Invalid cron expression: {e}")


def parse_cron_expression(cron_expr: str) -> dict:
    """解析并验证 Cron 表达式，返回人类可读描述"""
    parts = cron_expr.strip().split()
    if len(parts) != 5:
        raise ValueError(
            "Cron expression must have exactly 5 fields: minute hour day month weekday"
        )

    minute, hour, day, month, weekday = parts

    descriptions = []

    # Minute
    if minute == "*":
        descriptions.append("每分钟")
    elif "/" in minute:
        descriptions.append(f"每 {minute.split('/')[1]} 分钟")
    else:
        descriptions.append(f"第 {minute} 分")

    # Hour
    if hour == "*":
        descriptions.append("每小时")
    elif "/" in hour:
        descriptions.append(f"每 {hour.split('/')[1]} 小时")
    else:
        descriptions.append(f"{hour} 点")

    # Day
    if day == "*":
        pass  # 每天
    elif "/" in day:
        descriptions.append(f"每 {day.split('/')[1]} 天")
    else:
        descriptions.append(f"每月 {day} 日")

    # Month
    if month == "*":
        pass  # 每月
    elif "/" in month:
        descriptions.append(f"每 {month.split('/')[1]} 个月")
    else:
        descriptions.append(f"每年 {month} 月")

    # Weekday
    weekday_names = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]
    if weekday == "*":
        pass  # 每天
    elif "," in weekday:
        names = [weekday_names[int(w)] for w in weekday.split(",")]
        descriptions.append(f"每周 {', '.join(names)}")
    elif "-" in weekday:
        start, end = weekday.split("-")
        descriptions.append(
            f"每周 {weekday_names[int(start)]} 到 {weekday_names[int(end)]}"
        )
    elif "/" in weekday:
        descriptions.append(f"每 {weekday.split('/')[1]} 个星期")
    else:
        descriptions.append(f"每周 {weekday_names[int(weekday)]}")

    return {
        "expression": cron_expr,
        "description": "，".join(descriptions),
        "parts": {
            "minute": minute,
            "hour": hour,
            "day": day,
            "month": month,
            "weekday": weekday,
        },
    }
