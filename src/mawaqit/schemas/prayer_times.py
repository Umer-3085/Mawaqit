from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, validator
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

CALCULATION_METHODS = [
    "MUSLIM_WORLD_LEAGUE", "EGYPTIAN", "KARACHI", "UMM_AL_QURA",
    "DUBAI", "MOON_SIGHTING_COMMITTEE", "NORTH_AMERICA",
    "KUWAIT", "QATAR", "SINGAPORE", "UOIF"
]

MADHABS = ["SHAFI", "HANAFI"]

HIGH_LATITUDE_RULES = [
    "MIDDLE_OF_THE_NIGHT", "SEVENTH_OF_THE_NIGHT", "TWILIGHT_ANGLE"
]

class PrayerAdjustments(BaseModel):
    fajr: int = Field(0, ge=-60, le=60)
    sunrise: int = Field(0, ge=-60, le=60)
    dhuhr: int = Field(0, ge=-60, le=60)
    asr: int = Field(0, ge=-60, le=60)
    maghrib: int = Field(0, ge=-60, le=60)
    isha: int = Field(0, ge=-60, le=60)

class PrayerTimesResponse(BaseModel):
    date: str  # YYYY-MM-DD
    fajr: str
    sunrise: str
    dhuhr: str
    asr: str
    maghrib: str
    isha: str
    timezone: str
    calculation_method: str
    madhab: str

class PrayerTimesRangeResponse(BaseModel):
    items: list[PrayerTimesResponse]
    start_date: str
    end_date: str

class SingleDayParams(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
    date: Optional[date] = None  # defaults to today
    calculation_method: Optional[str] = Field("MUSLIM_WORLD_LEAGUE", pattern="^(" + "|".join(CALCULATION_METHODS) + ")$")
    madhab: Optional[str] = Field("SHAFI", pattern="^(" + "|".join(MADHABS) + ")$")
    high_latitude_rule: Optional[str] = Field("MIDDLE_OF_THE_NIGHT", pattern="^(" + "|".join(HIGH_LATITUDE_RULES) + ")$")
    timezone: str = Field(..., min_length=1)  # IANA timezone, validated in service
    adjustments: Optional[PrayerAdjustments] = None

    @validator("timezone")
    def validate_timezone(cls, v):
        try:
            ZoneInfo(v)
        except ZoneInfoNotFoundError:
            raise ValueError(f"Invalid timezone: {v}. Use IANA format like 'Asia/Karachi'")
        return v

class DateRangeParams(SingleDayParams):
    start_date: date
    end_date: date

    @validator("end_date")
    def validate_range(cls, v, values):
        if "start_date" in values and v < values["start_date"]:
            raise ValueError("end_date must be >= start_date")
        if "start_date" in values and (v - values["start_date"]).days > 30:
            raise ValueError("Date range cannot exceed 30 days")
        return v