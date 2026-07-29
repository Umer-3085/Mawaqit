
# Mawaqit Backend API - Functionality Overview

## Project Info

- **Name:** Mawaqit (مواقيت) — "Appointed Times"
- **Stack:** FastAPI (async), MySQL (aiomysql + SQLAlchemy 2.0), JWT Auth, Pydantic v2
- **Prayer Engine:** Embedded `adhanpy` (no external API)

---

## 1. Admin Module (JWT Auth)

| Method | Endpoint                          | Auth | Description                    |
| ------ | --------------------------------- | ---- | ------------------------------ |
| POST   | `/api/admin/login`              | ❌   | Username/password → JWT token |
| PATCH  | `/api/admin/change-credentials` | ✅   | Change username/password       |

---

## 2. Category Module

| Method | Endpoint                 | Auth | Description                                    |
| ------ | ------------------------ | ---- | ---------------------------------------------- |
| GET    | `/api/categories`      | ❌   | Paginated list                                 |
| GET    | `/api/categories/{id}` | ❌   | Single category                                |
| POST   | `/api/categories`      | ✅   | Create                                         |
| PUT    | `/api/categories/{id}` | ✅   | Update                                         |
| DELETE | `/api/categories/{id}` | ✅   | Delete (guarded: 400 if articles/videos exist) |

---

## 3. Subcategory Module

| Method | Endpoint                    | Auth | Description                                    |
| ------ | --------------------------- | ---- | ---------------------------------------------- |
| GET    | `/api/subcategories`      | ❌   | List (filter by`category_id`)                |
| GET    | `/api/subcategories/{id}` | ❌   | Single                                         |
| POST   | `/api/subcategories`      | ✅   | Create (validates`category_id`)              |
| PUT    | `/api/subcategories/{id}` | ✅   | Update                                         |
| DELETE | `/api/subcategories/{id}` | ✅   | Delete (guarded: 400 if articles/videos exist) |

---

## 4. Article/Video Module

*Type determined by `link` field: present → video, null → article*

| Method | Endpoint                                          | Auth | Description                                |
| ------ | ------------------------------------------------- | ---- | ------------------------------------------ |
| GET    | `/api/articles-videos`                          | ❌   | List (filter: category, subcategory, type) |
| GET    | `/api/articles-videos/category/{id}`            | ❌   | By category                                |
| GET    | `/api/articles-videos/subcategory/{id}`         | ❌   | By subcategory                             |
| GET    | `/api/articles-videos/video/category/{id}`      | ❌   | Videos by category                         |
| GET    | `/api/articles-videos/article/category/{id}`    | ❌   | Articles by category                       |
| GET    | `/api/articles-videos/video/subcategory/{id}`   | ❌   | Videos by subcategory                      |
| GET    | `/api/articles-videos/article/subcategory/{id}` | ❌   | Articles by subcategory                    |
| POST   | `/api/articles-videos`                          | ✅   | Create (auto-detects type)                 |
| PUT    | `/api/articles-videos/{id}`                     | ✅   | Update                                     |
| DELETE | `/api/articles-videos/{id}`                     | ✅   | Delete                                     |

---

## 5. Surah Module (Read-Only, Pre-populated 114)

| Method | Endpoint                             | Description                                  |
| ------ | ------------------------------------ | -------------------------------------------- |
| GET    | `/api/surahs`                      | Paginated, filter by revelation type, search |
| GET    | `/api/surahs/all`                  | Lightweight list of all 114                  |
| GET    | `/api/surahs/{number}`             | By number (1-114)                            |
| GET    | `/api/surahs/by-revelation/{type}` | Meccan/Medinan                               |
| GET    | `/api/surahs/search?q=`            | Search by name                               |

---

## 6. Verse Module (Read-Only, Pre-populated 6,236)

| Method | Endpoint                                  | Description                                  |
| ------ | ----------------------------------------- | -------------------------------------------- |
| GET    | `/api/verses`                           | Paginated, filter by surah, juz, page, sajda |
| GET    | `/api/verses/global/{number}`           | By global verse number (1-6236)              |
| GET    | `/api/verses/surah/{surah}`             | All verses of a surah                        |
| GET    | `/api/verses/surah/{surah}/ayah/{ayah}` | Specific verse                               |
| GET    | `/api/verses/juz/{juz}`                 | Verses by juz (1-30)                         |
| GET    | `/api/verses/page/{page}`               | Verses by page (1-604)                       |
| GET    | `/api/verses/sajda`                     | Sajda verses only                            |

---

## 7. Translation/Tafseer Details Module (Read-Only, 36 Records)

| Method | Endpoint                         | Description                                           |
| ------ | -------------------------------- | ----------------------------------------------------- |
| GET    | `/api/details`                 | Paginated (filter: language, direction, author, type) |
| GET    | `/api/details/all`             | All 36 records                                        |
| GET    | `/api/details/{id}`            | By ID                                                 |
| GET    | `/api/details/language/{lang}` | By language                                           |
| GET    | `/api/details/direction/{dir}` | By direction (ltr/rtl)                                |
| GET    | `/api/details/author/{author}` | By author                                             |

---

## 8. Verse Texts Module (Read-Only)

| Method | Endpoint                                                    | Description                                          |
| ------ | ----------------------------------------------------------- | ---------------------------------------------------- |
| GET    | `/api/texts`                                              | Paginated (filter: surah, ayah, detail_id, language) |
| GET    | `/api/texts/surah/{surah}`                                | All texts for a surah                                |
| GET    | `/api/texts/surah/{surah}/ayah/{ayah}`                    | All translations/tafseers for a verse                |
| GET    | `/api/texts/detail/{detail_id}`                           | All verses for a translation/tafseer                 |
| GET    | `/api/texts/language/{lang}`                              | By language                                          |
| GET    | `/api/texts/surah/{surah}/ayah/{ayah}/detail/{detail_id}` | Specific verse + translation                         |

---

## 9. Prayer Times Module (Runtime Calculation via `adhanpy`)

| Method | Endpoint                      | Key Params                                                                                                           |
| ------ | ----------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| GET    | `/api/prayer-times`         | `lat`, `lng`, `date?`, `timezone`, `calculation_method?`, `madhab?`, `high_latitude_rule?`, `*_adj?` |
| GET    | `/api/prayer-times/today`   | `lat`, `lng`, `timezone`, `calculation_method?`, `madhab?`, `high_latitude_rule?`                        |
| GET    | `/api/prayer-times/range`   | `lat`, `lng`, `start_date`, `end_date` (max 30 days), `timezone`, same optional params                     |
| GET    | `/api/prayer-times/methods` | Returns 11 calculation methods with descriptions                                                                     |

**Calculation Methods:** MUSLIM_WORLD_LEAGUE, EGYPTIAN, KARACHI, UMM_AL_QURA, DUBAI, MOON_SIGHTING_COMMITTEE, NORTH_AMERICA, KUWAIT, QATAR, SINGAPORE, UOIF
**Madhabs:** SHAFI, HANAFI
**High Latitude Rules:** MIDDLE_OF_THE_NIGHT, SEVENTH_OF_THE_NIGHT, TWILIGHT_ANGLE

---

## Data Status

| Entity                      | Count         | Source                                              |
| --------------------------- | ------------- | --------------------------------------------------- |
| Surahs                      | 114           | Pre-populated                                       |
| Verses                      | 6,236         | Pre-populated                                       |
| Translation/Tafseer Details | 36            | Pre-populated (1-32: translations, 33-38: tafseers) |
| Verse Texts                 | Full coverage | Seeded via`quran_seeder/`                         |
| Admins                      | Manual/seeder | —                                                  |

---

## Architecture

src/mawaqit/
├── models/          # SQLAlchemy 2.0 models
├── repositories/    # Data access layer
├── services/        # Business logic
├── schemas/         # Pydantic v2 request/response
├── api/             # FastAPI routers
│   ├── admin/
│   ├── category/
│   ├── subcategory/
│   ├── article_videos/
│   ├── surah/
│   ├── verse/
│   ├── detail/
│   ├── text/
│   └── prayer_times/
├── deps.py          # Dependency injection
├── main.py          # FastAPI app entry
└── config.py        # Settings

---

## Running the Server

```bash
uvicorn src.mawaqit.main:app --reload
# Swagger UI: http://localhost:8000/docs
# ReDoc:      http://localhost:8000/redoc
```
