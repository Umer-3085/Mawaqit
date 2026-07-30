from datetime import date, datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo
from adhanpy.PrayerTimes import PrayerTimes as AdhanPrayerTimes
from adhanpy.calculation.CalculationMethod import CalculationMethod
from adhanpy.calculation.CalculationParameters import CalculationParameters
from adhanpy.calculation.Madhab import Madhab
from adhanpy.calculation.HighLatitudeRule import HighLatitudeRule
from adhanpy.calculation.PrayerAdjustments import PrayerAdjustments as AdhanPrayerAdjustments
from adhanpy.util.TimeComponents import TimeComponents
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

        # Calculate nafl times
        nafl = self._calculate_nafl(pt, params.nafl_method)

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
            madhab=params.madhab,
            **nafl
        )

    def get_today(self, lat: float, lng: float, timezone: str,
                  calculation_method: str = "MUSLIM_WORLD_LEAGUE",
                  madhab: str = "SHAFI",
                  high_latitude_rule: str = "MIDDLE_OF_THE_NIGHT",
                  nafl_method: str = "QUARTER_DAY") -> PrayerTimesResponse:
        params = SingleDayParams(
            lat=lat, lng=lng, prayer_date=date.today(), timezone=timezone,
            calculation_method=calculation_method, madhab=madhab,
            high_latitude_rule=high_latitude_rule,
            nafl_method=nafl_method
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
                timezone=params.timezone, adjustments=params.adjustments,
                nafl_method=params.nafl_method
            )
            items.append(self._calculate_single(day_params))
            current += timedelta(days=1)
        return PrayerTimesRangeResponse(
            items=items,
            start_date=params.start_date.isoformat(),
            end_date=params.end_date.isoformat()
        )

    def _calculate_nafl(self, pt: AdhanPrayerTimes, method: str) -> dict:
        solar = pt._solar_time
        sunrise = pt.sunrise
        sunset = pt.sunset
        date_comp = pt._date_components
        
        transit_comp = TimeComponents.from_float(solar.transit).date_components(date_comp)
        day_len = sunset - sunrise
        
        ishraq = duha_start = ishraq_elev = duha_elev = None
        
        if method == "STANDARD_15MIN":
            ishraq = sunrise + timedelta(minutes=15)
            duha_start = sunrise + timedelta(minutes=15)
        elif method == "QUARTER_DAY":
            ishraq = sunrise + timedelta(minutes=15)
            duha_start = sunrise + day_len / 4
        elif method == "SOLAR_ANGLE_SPEAR":
            ishraq_comp = TimeComponents.from_float(solar.hour_angle(4.0, True))
            if ishraq_comp is None:
                raise RuntimeError("Solar calculation failed for ishraq angle")
            ishraq = ishraq_comp.date_components(date_comp)
            
            duha_comp = TimeComponents.from_float(solar.hour_angle(4.0, True))
            if duha_comp is None:
                raise RuntimeError("Solar calculation failed for duha angle")
            duha_start = duha_comp.date_components(date_comp)
            ishraq_elev = 4.0
            duha_elev = 4.0
        elif method == "SOLAR_ANGLE_DUHA":
            ishraq_comp = TimeComponents.from_float(solar.hour_angle(4.0, True))
            if ishraq_comp is None:
                raise RuntimeError("Solar calculation failed for ishraq angle")
            ishraq = ishraq_comp.date_components(date_comp)
            
            duha_comp = TimeComponents.from_float(solar.hour_angle(15.0, True))
            if duha_comp is None:
                raise RuntimeError("Solar calculation failed for duha angle")
            duha_start = duha_comp.date_components(date_comp)
            ishraq_elev = 4.0
            duha_elev = 15.0
        elif method == "MALIKI_DELAYED":
            ishraq_comp = TimeComponents.from_float(solar.hour_angle(7.0, True))
            if ishraq_comp is None:
                raise RuntimeError("Solar calculation failed for ishraq angle")
            ishraq = ishraq_comp.date_components(date_comp)
            duha_start = sunrise + day_len / 4
            ishraq_elev = 7.0
        
        def fmt(dt): return dt.strftime("%H:%M") if dt else None
        
        return {
            "ishraq": fmt(ishraq),
            "ishraq_elevation": ishraq_elev,
            "duha_start": fmt(duha_start),
            "duha_start_elevation": duha_elev,
            "duha_end": fmt(transit_comp),
            "awwabin_start": fmt(pt.maghrib),
            "awwabin_end": fmt(pt.isha),
            "nafl_method": method
        }

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