# Project Architecture Blueprint

**Generated**: 2026-01-19
**Version**: 1.9.1
**Status**: Implementation-Ready

## 1. Architecture Detection and Analysis

### Technology Stack
- **Language**: Python 3.12+
- **Web Framework**: FastAPI (Asynchronous, Type-Safe)
- **Data Processing**: NumPy, Pandas, Pyswisseph (Swiss Ephemeris)
- **Geospatial**: Geopy, Timezonefinder
- **Testing**: Pytest, Ruff
- **Containerization**: Docker
- **Package Management**: standard `pyproject.toml` (PEP 621)

### Architectural Pattern
- **Modular Monolith**: The application is structured as a single deployable unit but internally organized into distinct modules (`routers`, `services`, `utils`, `features`) with clear separation of concerns.
- **Layered Architecture**:
  1.  **Interface Layer** (`routers`): Handles HTTP requests, validation (Pydantic), and response formatting.
  2.  **Service Layer** (`services`, `features`): Encapsulates business logic, calculation engines, and external integrations.
  3.  **Domain/Data Layer** (`schemas`, `hd_constants`): Defines data models and immutable domain constants.
  4.  **Utility Layer** (`utils`): Shared cross-cutting concerns (logging, date manipulation, serialization).

## 2. Architectural Overview

The Human Design API is designed as a **high-precision calculation engine** exposed via validatable HTTP endpoints. The guiding principles are:
-   **Accuracy First**: Calculations (Swiss Ephemeris) must be precise to the second and arc-second.
-   **Statelessness**: No persistent database provided; the API acts as a pure function `Input -> Calculation -> Output`.
-   **Type Safety**: Strict Pydantic models for inputs and outputs ensure contract reliability.
-   **Transparency**: Responses include metadata about calculation context (Locality, UTC offsets).

## 3. Core Architectural Components

### A. Routers (`src/humandesign/routers`)
-   **Purpose**: Exposes API endpoints grouped by domain (`general`, `transits`, `composite`).
-   **Responsibility**: Input parsing, dependency injection (`verify_token`), invoking services, and mapping results to JSON.
-   **Interaction**: Calls `features` functions; depends on `schemas` for validation.

### B. Feature Engine (`src/humandesign/features`)
-   **Purpose**: The "Brain" of the application. Contains Rave Cosmology and Human Design algorithms.
-   **Internal Structure**:
    -   `core`: Ephemeris calculations, planetary positioning.
    -   `attributes`: Gates, Lines, Colors, Tones.
    -   `mechanics`: Auth determination, Channel definition, Type logic.
-   **Evolution**: Designed to be extensible for new calculation methods (e.g., Penta, Dream Rave) without breaking core logic.

### C. Utils (`src/humandesign/utils`)
-   **Purpose**: Specialized implementation details isolated from business logic.
-   **Components**:
    -   `calculations.py`: Shared heavy-lifting (e.g., `process_transit_data`, `enrich_transit_metadata`).
    -   `serialization.py`: Custom JSON encoders for NumPy types.
    -   `astrology.py`: Western zodiac conversions.

## 4. Data Architecture

-   **Domain Models**: Defined in `src/humandesign/schemas/input_models.py`. Pydantic classes enforce valid ranges (e.g., Month 1-12).
-   **Constants**: `src/humandesign/hd_constants.py` acts as the single source of truth for static domain data (Center names, Authority mappings, Variable dictionaries).
-   **Data Flow**:
    `HTTP Request` -> `Pydantic Model` -> `Feature Engine (NumPy/Pandas)` -> `Dict/Native Types` -> `JSON Response`

## 5. Cross-Cutting Concerns

-   **Authentication**: Bearer Token mechanism via `dependencies.verify_token`. Simple environment-based (`HD_API_TOKEN`) check.
-   **Error Handling**: Centralized `HTTPException` usage in routers. Validation errors returned automatically by FastAPI/Pydantic (`422 Unprocessable Entity`).
-   **Serialization**: Custom `NumpyEncoder` handles the impedance mismatch between calculation libraries (NumPy) and JSON output.

## 6. Service Communication Patterns

-   **Synchronous HTTP**: All processing is request-response based.
-   **Stateless**: No caching layer or database connection pooling required internally.
-   **Versioning**: Semantic Versioning (1.x.x) tracked in `pyproject.toml`.

## 7. Implementation Patterns

### Validation Patern
Use `Pydantic` with `pre=True` validators to offer "Forgiving Inputs" (coercing strings/leading zeros) while enforcing strict internal types.

### Calculation Pattern
**Input Tuple**: Standardized `(year, month, day, hour, minute, second, utc_offset)` tuple used across all HD functions for consistency.

### Metadata Enrichment Pattern (New in 1.9.x)
Use shared helpers (`enrich_transit_metadata`) to inject standardized context into different endpoints (Daily, Solar Return), ensuring consistent API surface area.

## 8. Development Blueprint

### Adding a New Calculation Endpoint
1.  **Define Schema**: Create Input/Output models in `schemas/`.
2.  **Implement Logic**: Add calculation function to `features/` (or `utils/` if composite).
3.  **Create Router**: Add endpoint to `routers/` using the schema.
4.  **Register Router**: Include in `api.py`.
5.  **Test**: Add integration test in `tests/`.

### Extending Metadata
1.  Update `enrich_transit_metadata` in `utils/calculations.py`.
2.  Update unit tests in `tests/test_utils_calculations.py`.
3.  Verify impact on `/transits/daily` and `/transits/solar_return`.
