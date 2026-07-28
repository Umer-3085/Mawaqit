from datetime import date, datetime
from typing import Optional
from zoneinfo import ZoneInfo
from adhanpy.PrayerTimes import PrayerTimes as AdhanPrayerTimes
from adhanpy.calculation.CalculationMethod import CalculationMethod
from adhanpy.calculation.CalculationParameters import CalculationParameters
from adhanpy.calculation.Madhab import Madhab
from adhanpy.calculation.HighLatitudeRule import HighLatitudeRule
from adhanpy.calculation.PrayerAdjustments import PrayerAdjustments as AdhanPrayerAdjustments
from mawaqit.schemas.prayer_times import (
    PrayerTimesResponse, PrayerTimesRangeResponse, PrayerAdjustments, SingleDayParams, DateRangeParams
)

class PrayerTimesService:
    def __init__(self):
        pass

    def _map_calculation_method(self, method_str: str) -> CalculationMethod:
        return CalculationMethod[method_str]

    def _map_madhab(self, madhab_str: str) -> Madhab:
        return Madhab[madhab_str]

    def _map_high_latitude_rule(self, rule_str: str) -> HighLatitudeRule:
        return HighLatitudeRule[rule_str]

    def _map_adjustments(self, adj: Optional[PrayerAdjustments]) -> Optional[AdhanPrayerAdjustments]:
        if adj is None:
            return None
        return AdhanPrayerAdjustments(
            fajr=adj.fajr, sunrise=adj.sunrise, dhuhr=adj.dhuhr,
            asr=adj.asr, maghrib=adj.maghrib, isha=adj.isha
        )

    def _calculate_single(self, params: SingleDayParams) -> PrayerTimesResponse:
        calc_method = self._map_calculation_method(params.calculation_method)
        madhab = self._map_madhab(params.madhab)
        high_lat_rule = self._map_high_latitude_rule(params.high_latitude_rule)
        adjustments = self._map_adjustments(params.adjustments)
        tz = ZoneInfo(params.timezone)

        # Build CalculationParameters
        calc_params = CalculationParameters(method=calc_method)
        calc_params.madhab = madhab
        calc_params.high_latitude_rule = high_lat_rule
        if adjustments:
            calc_params.adjustments = adjustments

        # Calculate
        target_date = params.prayer_date or datetime.now(tz).date()
        dt = datetime(target_date.year, target_date.month, target_date.day, tzinfo=tz)

        pt = AdhanPrayerTimes(
            coordinates=(params.lat, params.lng),
            date=dt,
            calculation_parameters=calc_params,
            time_zone=tz
        )

        # Format response
        def fmt(dt_obj: datetime) -> str:
            return dt_obj.strftime("%H:%M")

        return PrayerTimesResponse(
            date=target_date.isoformat(),
            fajr=fmt(pt.fajr),
            sunrise=fmt(pt.sunrise),
            dhuhr=fmt(pt.dhuhr),
            asr=fmt(pt.asr),
            maghrib=fmt(pt.maghrib),
            isha=fmt(pt.isha),
            timezone=params.timezone,
            calculation_method=params.calculation_method,
            madhab=params.madhab
        )

    def get_today(self, lat: float, lng: float, timezone: str,
                  calculation_method: str = "MUSLIM_WORLD_LEAGUE",
                  madhab: str = "SHAFI",
                  high_latitude_rule: str = "MIDDLE_OF_THE_NIGHT") -> PrayerTimesResponse:
        params = SingleDayParams(
            lat=lat, lng=lng, prayer_date=date.today(), timezone=timezone,
            calculation_method=calculation_method, madhab=madhab,
            high_latitude_rule=high_latitude_rule
        )
        return self._calculate_single(params)

    def get_by_date(self, params: SingleDayParams) -> PrayerTimesResponse:
        return self._calculate_single(params)

    def get_by_range(self, params: DateRangeParams) -> PrayerTimesRangeResponse:
        from datetime import timedelta
        items = []
        current = params.start_date
        while current <= params.end_date:
            day_params = SingleDayParams(
                lat=params.lat, lng=params.lng, prayer_date=current,
                calculation_method=params.calculation_method,
                madhab=params.madhab, high_latitude_rule=params.high_latitude_rule,
                timezone=params.timezone, adjustments=params.adjustments
            )
            items.append(self._calculate_single(day_params))
            current += timedelta(days=1)
        return PrayerTimesRangeResponse(
            items=items,
            start_date=params.start_date.isoformat(),
            end_date=params.end_date.isoformat()
        )

    def get_methods(self) -> list[dict]:
        """Return available calculation methods with descriptions"""
        return [
            {"value": "MUSLIM_WORLD_LEAGUE", "name": "Muslim World League", "fajr_angle": 18, "isha_angle": 17},
            {"value": "EGYPTIAN", "name": "Egyptian General Authority of Survey", "fajr_angle": 19.5, "isha_angle": 17.5},
            {"value": "KARACHI", "name": "University of Islamic Sciences, Karachi", "fajr_angle": 18, "isha_angle": 18},
            {"value": "UMM_AL_QURA", "name": "Umm al-Qura University, Makkah", "fajr_angle": 18.5, "isha_interval": 90},
            {"value": "DUBAI", "name": "Dubai / Gulf Region", "fajr_angle": 18.2, "isha_angle": 18.2},
            {"value": "MOON_SIGHTING_COMMITTEE", "name": "Moonsighting Committee", "fajr_angle": 18, "isha_angle": 18},
            {"value": "NORTH_AMERICA", "name": "ISNA / North America", "fajr_angle": 15, "isha_angle": 15},
            {"value": "KUWAIT", "name": "Kuwait", "fajr_angle": 18, "isha_angle": 17.5},
            {"value": "QATAR", "name": "Qatar", "fajr_angle": 18, "isha_interval": 90},
            {"value": "SINGAPORE", "name": "Singapore", "fajr_angle": 20, "isha_angle": 18},
            {"value": "UOIF", "name": "UOIF (France)", "fajr_angle": 12, "isha_angle": 12},
        ]