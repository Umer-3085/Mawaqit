# Nawafil Prayer Times Calculation Methods

This document describes the 5 scholarly calculation methods implemented for Nawafil (voluntary) prayer times in the Prayer Times API.

## Calculation Methods Comparison Table

| Method                      | Ishraq Calculation    | Duha Start Calculation      | Scholarly Basis                   | School/Tradition                        |
| --------------------------- | --------------------- | --------------------------- | --------------------------------- | --------------------------------------- |
| **STANDARD_15MIN**    | Sunrise + 15 minutes  | Sunrise + 15 minutes        | Fixed 15-min offset after sunrise | General/convenience                     |
| **QUARTER_DAY**       | Sunrise + 15 minutes  | Sunrise + (Day Length ÷ 4) | Quarter of daytime                | General                                 |
| **SOLAR_ANGLE_SPEAR** | Solar elevation 4.0° | Solar elevation 4.0°       | Height of a spear                 | Hanafi, Shāfiʿī                      |
| **SOLAR_ANGLE_DUHA**  | Solar elevation 4.0° | Solar elevation 15.0°      | 4° for Ishraq, 15° for Duha     | Hybrid (Hanafi/Shāfiʿī + later Duha) |
| **MALIKI_DELAYED**    | Solar elevation 7.0° | Sunrise + (Day Length ÷ 4) | Light spreads evenly              | Mālikī                                |

## Common Fields (All Methods)

| Field             | Calculation            | Notes                                                   |
| ----------------- | ---------------------- | ------------------------------------------------------- |
| `duha_end`      | Solar transit (midday) | `pt.transit` from adhanpy; Duha must end before Dhuhr |
| `awwabin_start` | Maghrib                | `pt.maghrib`; begins immediately after Maghrib        |
| `awwabin_end`   | Isha                   | `pt.isha`; ends at Isha prayer time                   |
