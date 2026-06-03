import os
from datetime import date, datetime
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import calendar

app = FastAPI(title="Holiday Date Checker API", version="1.0.0")

US_FEDERAL_HOLIDAYS = {
    "new_year": 1,
    "martin_luther_king": (1, "monday", 3),
    "presidents": (2, "monday", 3),
    "memorial": (5, "monday", "last"),
    "juneteenth": (6, 19),
    "independence": 7,
    "labor": (9, "monday", 1),
    "columbus": (10, "monday", 2),
    "veterans": 11,
    "thanksgiving": (11, "thursday", 4),
    "christmas": 12,
}

def get_nth_weekday(year: int, month: int, weekday: int, n: int) -> date:
    if n == "last":
        last_day = calendar.monthrange(year, month)[1]
        for day in range(last_day, 0, -1):
            d = date(year, month, day)
            if d.weekday() == weekday - 1:
                return d
    else:
        count = 0
        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            d = date(year, month, day)
            if d.weekday() == weekday - 1:
                count += 1
                if count == n:
                    return d
    return date(year, month, 1)

def calculate_holiday(year: int, holiday_key: str) -> date:
    if holiday_key == "new_year":
        return date(year, 1, 1)
    elif holiday_key == "martin_luther_king":
        return get_nth_weekday(year, 1, 1, 3)
    elif holiday_key == "presidents":
        return get_nth_weekday(year, 2, 1, 3)
    elif holiday_key == "memorial":
        return get_nth_weekday(year, 5, 1, "last")
    elif holiday_key == "juneteenth":
        return date(year, 6, 19)
    elif holiday_key == "independence":
        return date(year, 7, 4)
    elif holiday_key == "labor":
        return get_nth_weekday(year, 9, 1, 1)
    elif holiday_key == "columbus":
        return get_nth_weekday(year, 10, 1, 2)
    elif holiday_key == "veterans":
        return date(year, 11, 11)
    elif holiday_key == "thanksgiving":
        return get_nth_weekday(year, 11, 4, 4)
    elif holiday_key == "christmas":
        return date(year, 12, 25)
    return date(year, 1, 1)

def get_all_holidays(year: int) -> dict:
    return {holiday: calculate_holiday(year, holiday) for holiday in US_FEDERAL_HOLIDAYS}

def get_api_key(x_api_key: str = None):
    expected_key = os.environ.get("HOLIDAY_API_KEY", "dev-key")
    if x_api_key != expected_key and expected_key != "dev-key":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

class DateCheck(BaseModel):
    date: str

class HolidayCheckResponse(BaseModel):
    date: str
    formatted_date: str
    is_holiday: bool
    holiday_name: str | None
    day_of_week: str

class HolidaysInMonth(BaseModel):
    year: int
    month: int

class MonthHolidaysResponse(BaseModel):
    year: int
    month: int
    holidays: list

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/check")
def check_holiday(data: DateCheck, api_key: str = Depends(get_api_key)):
    try:
        check_date = datetime.strptime(data.date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    holidays = get_all_holidays(check_date.year)
    holiday_name = None
    for name, h_date in holidays.items():
        if h_date == check_date:
            holiday_name = name.replace("_", " ").title()
            break
    return HolidayCheckResponse(
        date=data.date, formatted_date=check_date.strftime("%B %d, %Y"),
        is_holiday=holiday_name is not None, holiday_name=holiday_name,
        day_of_week=check_date.strftime("%A")
    )

@app.post("/month")
def holidays_in_month(data: HolidaysInMonth, api_key: str = Depends(get_api_key)):
    if data.month < 1 or data.month > 12:
        raise HTTPException(status_code=400, detail="Invalid month (1-12)")
    holidays = get_all_holidays(data.year)
    month_holidays = []
    for name, h_date in holidays.items():
        if h_date.month == data.month:
            month_holidays.append({
                "name": name.replace("_", " ").title(),
                "date": h_date.isoformat(),
                "formatted": h_date.strftime("%B %d, %Y")
            })
    return MonthHolidaysResponse(year=data.year, month=data.month, holidays=sorted(month_holidays, key=lambda x: x["date"]))

@app.post("/range")
def holidays_in_range(start_date: str, end_date: str, api_key: str = Depends(get_api_key)):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    if start > end:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    holidays_in_range = []
    for year in range(start.year, end.year + 1):
        holidays = get_all_holidays(year)
        for name, h_date in holidays.items():
            if start <= h_date <= end:
                holidays_in_range.append({
                    "name": name.replace("_", " ").title(),
                    "date": h_date.isoformat(),
                    "formatted": h_date.strftime("%B %d, %Y")
                })
    return {"start": start_date, "end": end_date, "holidays": sorted(holidays_in_range, key=lambda x: x["date"])}

@app.get("/years/{year}")
def holidays_in_year(year: int, api_key: str = Depends(get_api_key)):
    if year < 1900 or year > 2100:
        raise HTTPException(status_code=400, detail="Year out of range (1900-2100)")
    holidays = get_all_holidays(year)
    return {"year": year, "holidays": [{"name": name.replace("_", " ").title(), "date": str(h_date)} for name, h_date in sorted(holidays.items(), key=lambda x: x[1])]}