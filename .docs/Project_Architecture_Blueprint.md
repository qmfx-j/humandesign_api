# Project Architecture Blueprint

**Date Generated:** 2025-12-22  
**Version:** 1.2.4  
**Status:** Implementation-Ready

---

## 1. Architecture Detection and Analysis

**Project Type:** Python (FastAPI)  
**Architecture Pattern:** Layered Monolith  
**Tech Stack:**
-   **Framework**: FastAPI (Async Web Framework)
-   **Language**: Python 3.12+
-   **Core Logic**: `pyswisseph` (Astrology), `numpy`, `pandas`
-   **Utilities**: `geopy` (Geocoding), `timezonefinder` (Timezone Resolution)
-   **Formatting**: `matplotlib` (Charting), custom JSON converters
-   **Deployment**: Docker & Docker Compose

## 2. Architectural Overview

The **Human Design API** is designed as a stateless, containerized microservice that calculates and serves Human Design astrological data. It follows a predictable layered structure where:
1.  **Transport Layer (`api.py`)**: Handles HTTP requests, validation (Pydantic), and response formatting.
2.  **Service/Logic Layer (`hd_features.py`, `composite_handler.py`)**: Encapsulates the core domain logic (planetary calculations, bodygraph mechanics).
3.  **Data/Constants Layer (`hd_constants.py`)**: Stores static domain data (Gate/Line definitions, profiles).
4.  **Presentation Layer (`convertJSON.py`, `chart.py`)**: Formats raw calculation data into user-friendly JSON or visual diagrams.

The architecture emphasizes **correctness** (using Swiss Ephemeris) and **ease of deployment** (Docker).

## 3. Core Architectural Components

### A. API Gateway / Transport (`api.py`)
-   **Purpose**: Entry point for all interactions. Defines REST endpoints.
-   **Responsibilities**:
    -   Input validation (Pydantic models).
    -   Geocoding & Timezone resolution (Middleware-like behavior).
    -   Orchestrating calls to the Calculation Engine.
    -   Standardizing responses (ISO 8601 Dates, JSON structure).
-   **Key Endpoints**:
    -   `/calculate`: Single person analysis.
    -   `/bodygraph`: Image generation.
    -   `/transits/*`: Daily and Solar Return forecasting.
    -   `/compmatrix`: Multi-person composite analysis.

### B. Calculation Engine (`hd_features.py`)
-   **Purpose**: The "Brain" of the system.
-   **Responsibilities**:
    -   Interfacing with `pyswisseph` for planetary positions.
    -   Converting astronomical data to Human Design Gates/Lines.
    -   Determining Channels, Centers, Definition, and Type.
-   **Pattern**: Object-Oriented wrapper (`hd_features` class) around procedural calculation logic.

### C. Composite Logic (`composite_handler.py`)
-   **Purpose**: Handling interactions between multiple charts.
-   **Responsibilities**:
    -   Batch processing of input profiles.
    -   Calculating electromagnetic connections (Composite Charts).
    -   Normalizing output for the matrix endpoint.

### D. Visualization & Formatting (`chart.py`, `convertJSON.py`)
-   **Purpose**: Transform raw data into consumable formats.
-   **Responsibilities**:
    -   `chart.py`: Generating PNG/SVG images of the BodyGraph.
    -   `convertJSON.py`: specialized JSON serialization (handling `numpy` types) and rounding.

## 4. Architectural Layers and Dependencies

1.  **Interface Layer**: `api.py`
    *   *Depends on*: Logic Layer, Formatting Layer, Infrastructure.
2.  **Logic Logic**: `hd_features.py`, `composite_handler.py`
    *   *Depends on*: Data Layer (`hd_constants.py`), Low-level Libs (`swe`).
3.  **Formatting Layer**: `convertJSON.py`, `chart.py`
    *   *Depends on*: Data Layer.
4.  **Data Layer**: `hd_constants.py` (Static DB).

**Data Flow**:
`Request -> API (Validate/Geocode) -> Logic (Calculate) -> Formatting (JSON/Image) -> Response`

## 5. Deployment Architecture

-   **Containerization**: Single Docker container (`Dockerfile`) encapsulating Python runtime and compiled C-extensions (`pyswisseph`).
-   **Orchestration**: `docker-compose.yml` for local development and simplified deployment.
-   **Configuration**: Environment variables (e.g., `HD_API_TOKEN`) loaded via `.env` file.
-   **Optimization**: Multi-stage build process to minimize image size by stripping build artifacts.

## 6. Implementation Patterns

### ISO 8601 Date Standardization
-   All dates are converted to UTC and formatted as `YYYY-MM-DDTHH:MM:SSZ`.
-   **Implementation**: Global helper functions in `api.py` (`to_iso_utc`, `clean_birth_date_to_iso`) handle conversion from internal tuple formats or raw strings.

### Pydantic Validation
-   Strict type checking with flexible input coercion (turning string `"00"` into int `0`).
-   Custom validators for range checking (Years 1800-2100).

### Definition Calculation (Graph Traversal)
-   Uses Depth-First Search (DFS) to determine definition type (Single, Split, etc.) by analyzing connected components in the BodyGraph.

## 7. Extension Guidelines

-   **Adding New Endpoints**: Define new route in `api.py`, add validation model.
-   **New Calculations**: Implement method in `hd_features.py`, expose via `api.py`.
-   **Visualization**: Update `layout_data.json` for new geometries, update `chart.py` renderer.

## 8. Development & Release Workflow

-   **Versioning**: Managed in `pyproject.toml`.
-   **Changelog**: `CHANGELOG.md` updated per release.
-   **Build**: Automated via `.docs/build_docker.sh`.

---
*Generated by Release Manager Agent for Human Design API v1.2.4*
