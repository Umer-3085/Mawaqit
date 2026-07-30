from __future__ import annotations
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

CALCULATION_METHODS = [
    "MUSLIM_WORLD_LEAGUE",
    "EGYPTIAN",
    "KARACHI",
    "UMM_AL_QURA",
    "DUBAI",
    "MOON_SIGHTING_COMMITTEE",
    "NORTH_AMERICA",
    "KUWAIT",
    "QATAR",
    "SINGAPORE",
    "UOIF",
]

MADHABS = ["SHAFI", "HANAFI"]

HIGH_LATITUDE_RULES = ["MIDDLE_OF_THE_NIGHT", "SEVENTH_OF_THE_NIGHT", "TWILIGHT_ANGLE"]

NAFL_METHODS = [
    "STANDARD_15MIN",
    "QUARTER_DAY",
    "SOLAR_ANGLE_SPEAR",
    "SOLAR_ANGLE_DUHA",
    "MALIKI_DELAYED",
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
    ishraq: Optional[str] = None
    ishraq_elevation: Optional[float] = None
    duha_start: Optional[str] = None
    duha_start_elevation: Optional[float] = None
    duha_end: Optional[str] = None
    awwabin_start: Optional[str] = None
    awwabin_end: Optional[str] = None
    nafl_method: Optional[str] = None


class PrayerTimesRangeResponse(BaseModel):
    items: list[PrayerTimesResponse]
    start_date: str
    end_date: str


class SingleDayParams(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
    # Renamed field to avoid collision with datetime.date
    prayer_date: Optional[date] = Field(
        default=None, description="Date (YYYY-MM-DD), defaults to today"
    )
    calculation_method: str = Field(
        "MUSLIM_WORLD_LEAGUE", pattern="^(" + "|".join(CALCULATION_METHODS) + ")$"
    )
    madhab: str = Field("SHAFI", pattern="^(" + "|".join(MADHABS) + ")$")
    high_latitude_rule: str = Field(
        "MIDDLE_OF_THE_NIGHT", pattern="^(" + "|".join(HIGH_LATITUDE_RULES) + ")$"
    )
    timezone: str = Field(..., min_length=1)
    adjustments: Optional[PrayerAdjustments] = None
    nafl_method: str = Field("QUARTER_DAY", pattern="^(" + "|".join(NAFL_METHODS) + ")$")

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        try:
            ZoneInfo(v)
        except ZoneInfoNotFoundError:
            raise ValueError(f"Invalid timezone: {v}. Use IANA format like 'Asia/Karachi'")
        return v


class DateRangeParams(SingleDayParams):
    start_date: date
    end_date: date

    @field_validator("end_date")
    @classmethod
    def validate_range(cls, v: date, info) -> date:
        if "start_date" in info.data and v < info.data["start_date"]:
            raise ValueError("end_date must be >= start_date")
        if "start_date" in info.data and (v - info.data["start_date"]).days > 30:
            raise ValueError("Date range cannot exceed 30 days")
        return v
