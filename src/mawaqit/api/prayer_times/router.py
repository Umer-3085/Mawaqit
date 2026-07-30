from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import ValidationError
from datetime import date
from mawaqit.schemas.prayer_times import (
    NAFL_METHODS, PrayerTimesResponse, PrayerTimesRangeResponse, SingleDayParams, DateRangeParams
)
from mawaqit.services.prayer_times import PrayerTimesService
from mawaqit.schemas.prayer_times import PrayerAdjustments
from mawaqit.api.deps import get_prayer_times_service

router = APIRouter(prefix="/prayer-times", tags=["Prayer Times"])

@router.get("", response_model=PrayerTimesResponse)
async def get_prayer_times(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lng: float = Query(..., ge=-180, le=180, description="Longitude"),
    date: date | None = Query(None, description="Date (YYYY-MM-DD), defaults to today"),
    calculation_method: str = Query("MUSLIM_WORLD_LEAGUE"),
    madhab: str = Query("SHAFI"),
    high_latitude_rule: str = Query("MIDDLE_OF_THE_NIGHT"),
    timezone: str = Query(..., description="IANA timezone, e.g., Asia/Karachi"),
    fajr_adj: int = Query(0, ge=-60, le=60),
    sunrise_adj: int = Query(0, ge=-60, le=60),
    dhuhr_adj: int = Query(0, ge=-60, le=60),
    asr_adj: int = Query(0, ge=-60, le=60),
    maghrib_adj: int = Query(0, ge=-60, le=60),
    isha_adj: int = Query(0, ge=-60, le=60),
    service: PrayerTimesService = Depends(get_prayer_times_service),
    nafl_method: str = Query("QUATER_DAY", enum=NAFL_METHODS)
):
    try:
        params = SingleDayParams(
            lat=lat, lng=lng, prayer_date=date,  # <-- fix: prayer_date not date
            calculation_method=calculation_method,
            madhab=madhab, high_latitude_rule=high_latitude_rule, timezone=timezone,
            nafl_method=nafl_method,
            adjustments=PrayerAdjustments(
                fajr=fajr_adj,
                sunrise=sunrise_adj,
                dhuhr=dhuhr_adj,
                asr=asr_adj,
                maghrib=maghrib_adj,
                isha=isha_adj,
            ),
        )
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    return service.get_by_date(params)

@router.get("/today", response_model=PrayerTimesResponse)
async def get_today_prayer_times(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    timezone: str = Query(..., description="IANA timezone, e.g., Asia/Karachi"),
    calculation_method: str = Query("MUSLIM_WORLD_LEAGUE"),
    madhab: str = Query("SHAFI"),
    high_latitude_rule: str = Query("MIDDLE_OF_THE_NIGHT"),
    service: PrayerTimesService = Depends(get_prayer_times_service),
    nafl_method: str = Query("QUATER_DAY", enum=NAFL_METHODS)
):
    return service.get_today(lat, lng, timezone, calculation_method, madhab, high_latitude_rule)

@router.get("/range", response_model=PrayerTimesRangeResponse)
async def get_prayer_times_range(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    start_date: date = Query(...),
    end_date: date = Query(...),
    calculation_method: str = Query("MUSLIM_WORLD_LEAGUE"),
    madhab: str = Query("SHAFI"),
    high_latitude_rule: str = Query("MIDDLE_OF_THE_NIGHT"),
    timezone: str = Query(...),
    service: PrayerTimesService = Depends(get_prayer_times_service),
    nafl_method: str = Query("QUATER_DAY", enum=NAFL_METHODS)
):
    try:
        params = DateRangeParams(
            lat=lat, lng=lng,
            start_date=start_date,
            end_date=end_date,
            calculation_method=calculation_method,
            madhab=madhab, high_latitude_rule=high_latitude_rule, timezone=timezone,
            adjustments=None,nafl_method=nafl_method
        )
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    return service.get_by_range(params)

@router.get("/methods")
async def get_calculation_methods(
    service: PrayerTimesService = Depends(get_prayer_times_service)
):
    return service.get_methods()