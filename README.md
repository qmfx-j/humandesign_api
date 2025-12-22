# Human Design API

Welcome to the Human Design API! This project provides a robust and scalable API for calculating various Human Design features based on birth data. Built with FastAPI and leveraging powerful astrological and geographical libraries, it offers a comprehensive solution for integrating Human Design analytics into your applications.

## Project Overview
 
The **Human Design API** is a high-performance Python service meant to power modern Human Design applications. It serves as a comprehensive backend engine that:

1.   **Calculates** core and deep Human Design metrics from birth data (Earth, Moon, Nodes, Planets, Gates, Lines, Color, Tone, Base).
2.  **Resolves** birth locations to precise geocoordinates and timezones automatically.
3.  **Visualizes** results by generating beautiful, high-quality BodyGraph images on-the-fly.

Whether you are building a mobile app, a professional dashboard, or a personal research tool, this API provides the rigorous astrological data and visual assets you need, all containerized for easy deployment.

### Key Features:

*   **FastAPI Backend**: High-performance, async-ready Python web framework.
*   **Precise Calculations**: Uses `pyswisseph` for Swiss Ephemeris accuracy and `geopy`/`timezonefinder` for reliable location and timezone resolution.
*   **BodyGraph Visualization**: Generates high-fidelity, transparent BodyGraph charts in PNG, SVG, and JPG formats via the `/bodygraph` endpoint.
*   **Composite Analysis**: Calculates relationship mechanics (connection channels, centers) between multiple people via the `/compmatrix` endpoint.
*   **Transit Analysis**: Provides Daily Weather and Solar Return (Yearly Theme) calculations for advanced forecasting.
*   **Comprehensive Chart Data**: Returns Energy Type, Strategy, Authority, Profile, Incarnation Cross, Variables, and full Planetary/Gate positions (Gate, Line, Color, Tone, Base).
*   **Robust Validation**: Strict input validation using Pydantic, supporting flexible data types (integers or strings) for ease of integration.
*   **Docker Ready**: Simple deployment with Docker and Docker Compose.
*   **OpenAPI Specification**: Fully documented API with `openapi.yaml` and interactive Swagger UI.
*   **Authentication**: Secure access via Bearer token.

## Installation and Setup

To get the Human Design API up and running, follow these steps:

### Prerequisites

*   **Docker**: Ensure Docker is installed and running on your system. You can download it from [Docker's official website](https://www.docker.com/products/docker-desktop).
*   **Docker Compose**: Docker Compose is usually bundled with Docker Desktop. Verify its installation by running `docker-compose --version` in your terminal.

### Steps

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repo/humandesign_api.git
    cd humandesign_api
    ```

2.  **Environment Variables**:
    Create a `.env` file in the root directory of the project based on the `.env_example` file. This file will store your API token.

    ```
    HD_API_TOKEN=your_secret_token_here
    ```
    Replace `your_secret_token_here` with a strong, unique token.

3.  **Build and Run with Docker Compose**:
    Navigate to the project root directory in your terminal and run:

    ```bash
    docker-compose up --build -d
    ```
    *   `--build`: This flag tells Docker Compose to build the images before starting containers. This is necessary for the first run or after any changes to the `Dockerfile` or `requirements.txt`.
    *   `-d`: This flag runs the containers in detached mode, meaning they will run in the background.

4.  **Verify Installation**:
    Once the containers are up, the API should be accessible at `http://localhost:9021`. You can verify its status by checking your Docker Desktop dashboard or by running:

    ```bash
    docker ps
    ```
    You should see a container named `humandesignapi` running.

## Folder Structure

The project is organized as follows:

```
.
├── .env_example
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
├── api.py
├── chart.py
├── composite_handler.py
├── convertJSON.py
├── docker-compose.yml
├── Dockerfile
├── geocode.py
├── hd_constants.py
├── hd_features.py
├── layout_data.json
├── openapi.yaml
├── requirements.txt
├── static/
│   └── favicon.ico
└── pyproject.toml
```

*   **`api.py`**: The main FastAPI application. Defines endpoints, handles requests, and integrates calculation and visualization logic.
*   **`chart.py`**:  Generates high-fidelity BodyGraph images (PNG, SVG, JPG) using `matplotlib` and extracted vector geometry.
*   **`composite_handler.py`**: Encapsulates logic for composite chart calculations, including input processing and feature enrichment.
*   **`convertJSON.py`**: Utility functions for formatting calculation results into structured JSON.
*   **`docker-compose.yml`**: Orchestrates the Docker service for easy deployment.
*   **`Dockerfile`**: Defines the container environment for the API.
*   **`geocode.py`**: Handles geocoding and timezone resolution.
*   **`hd_constants.py`**: Stores Human Design constants, mappings, and databases.
*   **`hd_features.py`**: Core logic for Human Design astrological calculations.
*   **`layout_data.json`**: Contains precise SVG paths and coordinates for rendering the BodyGraph.
*   **`openapi.yaml`**: The OpenAPI 3.0 specification file for the API.
*   **`requirements.txt`**: Python dependencies.
*   **`pyproject.toml`**: Standard configuration file for project metadata and dependencies, including the single source of truth for the project version.
*   **`CHANGELOG.md`**: Records all notable changes to the project.
*   **`LICENSE`**: Project license.
*   **`README.md`**: Project documentation (this file).
*   **`.env_example`**: Template for environment variables.
*   **`static/`**: Static assets directory.

## API Usage

The Human Design API provides a single endpoint for calculating Human Design features.

### `GET /calculate`

Calculates Human Design features based on birth information.

#### Parameters

| Name     | Type    | Description                                     | Required |
| :------- | :------ | :---------------------------------------------- | :------- |
| `year`   | `integer` | Birth year (e.g., `1990`)                       | Yes      |
| `month`  | `integer` | Birth month (e.g., `7` for July)                | Yes      |
| `day`    | `integer` | Birth day (e.g., `15`)                          | Yes      |
| `hour`   | `integer` | Birth hour (24-hour format, e.g., `14` for 2 PM) | Yes      |
| `minute` | `integer` | Birth minute (e.g., `30`)                       | Yes      |
| `second` | `integer` | Birth second (optional, default `0`)            | No       |
| `place`  | `string`  | Birth place (city, country, e.g., `London, UK`) | Yes      |

#### Authentication

This endpoint requires an API token passed in the `Authorization` header as a Bearer token.

`Authorization: Bearer your_secret_token_here`

#### Example Request

```bash
curl -X GET "http://localhost:9021/calculate?year=1990&month=7&day=15&hour=14&minute=30&place=London%2C%20UK" \
     -H "Authorization: Bearer your_secret_token_here"
```

### `GET /bodygraph`

Generates a visual BodyGraph chart image based on birth information.

### `GET /transits/daily`

Calculates the "Weather of the Day" (Transit Analysis).

#### Parameters
*   Birth Data (year, month, day, hour, minute, place)
*   Transit Date (`transit_year`, `transit_month`, `transit_day`)

### `GET /transits/solar_return`

Calculates the "Yearly Theme" (Solar Return Analysis).

#### Parameters
*   Birth Data (year, month, day, hour, minute, place)
*   Offset (`sr_year_offset`): Years after birth (e.g., 1 for 1st birthday return).

### `POST /compmatrix`

Calculates the composite Human Design matrix for two or more people.

#### Request Body
The body should be a dictionary where keys are person identifiers (e.g., `person1`, `person2`) and values are their birth details.

**Flexible Inputs**: Numeric fields (`year`, `month`, `day`, `hour`, `minute`) accept both **integers** (e.g., `1990`) and **strings** (e.g., `"1990"`, `"00"`).

```json
{
  "person1": {
    "place": "Berlin, Germany",
    "year": 1985,
    "month": 6,
    "day": 15,
    "hour": 14,
    "minute": "00"
  },
  "person2": {
    "place": "Munich, Germany",
    "year": "1988",
    "month": 11,
    "day": 22,
    "hour": 9,
    "minute": 15
  }
}
```

#### Authentication
Requires Bearer token in `Authorization` header.

#### Example Response
Returns a comprehensive analysis including individual profiles and the composite connection type (e.g., "Split Definition", "Work to do").

```bash
curl -X 'POST' \
  'http://localhost:9021/compmatrix' \
  -H 'Authorization: Bearer your_token' \
  -H 'Content-Type: application/json' \
  -d '{...}'
```

#### Parameters

| Name     | Type    | Description                                     | Required |
| :------- | :------ | :---------------------------------------------- | :------- |
| `year`   | `integer` | Birth year (e.g., `1990`)                       | Yes      |
| `month`  | `integer` | Birth month (e.g., `7` for July)                | Yes      |
| `day`    | `integer` | Birth day (e.g., `15`)                          | Yes      |
| `hour`   | `integer` | Birth hour (24-hour format, e.g., `14` for 2 PM) | Yes      |
| `minute` | `integer` | Birth minute (e.g., `30`)                       | Yes      |
| `second` | `integer` | Birth second (optional, default `0`)            | No       |
| `place`  | `string`  | Birth place (city, country, e.g., `London, UK`) | Yes      |
| `fmt`    | `string`  | Image format: `png`, `svg`, `jpg`, `jpeg` (default: `png`) | No       |

#### Authentication

This endpoint requires an API token passed in the `Authorization` header as a Bearer token.

`Authorization: Bearer your_secret_token_here`

#### Example Request

```bash
curl -X GET "http://localhost:9021/bodygraph?year=1990&month=7&day=15&hour=14&minute=30&place=London%2C%20UK&fmt=png" \
     -H "Authorization: Bearer your_secret_token_here" \
     -o bodygraph.png
```

#### Response

Returns the image file directly (MIME type `image/png`, `image/svg+xml`, or `image/jpeg`).

<p align="center">
  <img src="static/bodygraph_sample.png" width="50%" />
</p>

#### Example Response

```json
{
  "general": {
    "birth_date": "1990-07-15T13:30:00Z",
    "create_date": "1990-04-15T00:56:00Z",
    "place": "London, UK",
    "energy_type": "Projector",
    "strategy": "Wait for the Invitation",
    "signature": "Success",
    "not_self": "Bitterness",
    "aura": "Focused & Absorbing",
    "inner_authority": "Solar Plexus",
    "inc_cross": "The Right Angle Cross of the Maya (2)",
    "profile": "3/5: Martyr Heretic",
    "defined_centers": [
      "Throat",
      "Root",
      "G_Center",
      "SolarPlexus"
    ],
    "undefined_centers": [
      "Heart",
      "Ajna",
      "Spleen",
      "Head",
      "Sacral"
    ],
    "definition": "Split Definition",
    "variables": {
      "right_up": "right",
      "right_down": "left",
      "left_up": "right",
      "left_down": "right"
    }
  },
  "gates": {
    "prs": {
      "Planets": [
        {
          "Planet": "Sun",
          "Lon": 112.806,
          "Gate": 62,
          "Line": 3,
          "Color": 2,
          "Tone": 1,
          "Base": 5,
          "Ch_Gate": 0
        },
        {
          "Planet": "Earth",
          "Lon": 292.8057828170957,
          "Gate": 61,
          "Line": 3,
          "Color": 2,
          "Tone": 1,
          "Base": 5,
          "Ch_Gate": 0
        },
        {
          "Planet": "Moon",
          "Lon": 24.13491606652376,
          "Gate": 42,
          "Line": 4,
          "Color": 4,
          "Tone": 4,
          "Base": 5,
          "Ch_Gate": 0
        },
        {
          "Planet": "North_Node",
          "Lon": 307.35906010943785,
          "Gate": 41,
          "Line": 6,
          "Color": 5,
          "Tone": 2,
          "Base": 4,
          "Ch_Gate": 30
        },
        {
          "Planet": "South_Node",
          "Lon": 127.35906010943785,
          "Gate": 31,
          "Line": 6,
          "Color": 5,
          "Tone": 2,
          "Base": 4,
          "Ch_Gate": 7
        },
        {
          "Planet": "Mercury",
          "Lon": 126.89036485434069,
          "Gate": 31,
          "Line": 6,
          "Color": 2,
          "Tone": 2,
          "Base": 4,
          "Ch_Gate": 7
        },
        {
          "Planet": "Venus",
          "Lon": 84.48623656115177,
          "Gate": 12,
          "Line": 2,
          "Color": 6,
          "Tone": 6,
          "Base": 3,
          "Ch_Gate": 0
        },
        {
          "Planet": "Mars",
          "Lon": 31.983961512449053,
          "Gate": 3,
          "Line": 6,
          "Color": 6,
          "Tone": 6,
          "Base": 2,
          "Ch_Gate": 0
        },
        {
          "Planet": "Jupiter",
          "Lon": 112.56310904422688,
          "Gate": 62,
          "Line": 2,
          "Color": 6,
          "Tone": 4,
          "Base": 4,
          "Ch_Gate": 0
        },
        {
          "Planet": "Saturn",
          "Lon": 291.95899818771164,
          "Gate": 61,
          "Line": 2,
          "Color": 2,
          "Tone": 5,
          "Base": 3,
          "Ch_Gate": 0
        },
        {
          "Planet": "Uranus",
          "Lon": 276.9643234363261,
          "Gate": 58,
          "Line": 4,
          "Color": 2,
          "Tone": 5,
          "Base": 4,
          "Ch_Gate": 0
        },
        {
          "Planet": "Neptune",
          "Lon": 282.9195480234818,
          "Gate": 38,
          "Line": 4,
          "Color": 4,
          "Tone": 6,
          "Base": 2,
          "Ch_Gate": 0
        },
        {
          "Planet": "Pluto",
          "Lon": 224.99913456990504,
          "Gate": 1,
          "Line": 2,
          "Color": 6,
          "Tone": 2,
          "Base": 1,
          "Ch_Gate": 0
        }
      ]
    },
    "des": {
      "Planets": [
        {
          "Planet": "Sun",
          "Lon": 24.805782817306426,
          "Gate": 42,
          "Line": 5,
          "Color": 2,
          "Tone": 6,
          "Base": 4,
          "Ch_Gate": 0
        },
        {
          "Planet": "Earth",
          "Lon": 204.80578281730644,
          "Gate": 32,
          "Line": 5,
          "Color": 2,
          "Tone": 6,
          "Base": 4,
          "Ch_Gate": 0
        },
        {
          "Planet": "Moon",
          "Lon": 258.3863670444505,
          "Gate": 26,
          "Line": 2,
          "Color": 3,
          "Tone": 6,
          "Base": 2,
          "Ch_Gate": 0
        },
        {
          "Planet": "North_Node",
          "Lon": 313.3571239367391,
          "Gate": 13,
          "Line": 1,
          "Color": 1,
          "Tone": 5,
          "Base": 1,
          "Ch_Gate": 0
        },
        {
          "Planet": "South_Node",
          "Lon": 133.35712393673907,
          "Gate": 7,
          "Line": 1,
          "Color": 1,
          "Tone": 5,
          "Base": 1,
          "Ch_Gate": 31
        },
        {
          "Planet": "Mercury",
          "Lon": 44.12339096446304,
          "Gate": 2,
          "Line": 1,
          "Color": 6,
          "Tone": 4,
          "Base": 3,
          "Ch_Gate": 0
        },
        {
          "Planet": "Venus",
          "Lon": 339.05797731425446,
          "Gate": 37,
          "Line": 4,
          "Color": 4,
          "Tone": 2,
          "Base": 1,
          "Ch_Gate": 0
        },
        {
          "Planet": "Mars",
          "Lon": 325.59927235501266,
          "Gate": 30,
          "Line": 2,
          "Color": 2,
          "Tone": 1,
          "Base": 2,
          "Ch_Gate": 41
        },
        {
          "Planet": "Jupiter",
          "Lon": 94.4824157445859,
          "Gate": 52,
          "Line": 1,
          "Color": 4,
          "Tone": 6,
          "Base": 2,
          "Ch_Gate": 0
        },
        {
          "Planet": "Saturn",
          "Lon": 295.01454195131396,
          "Gate": 61,
          "Line": 5,
          "Color": 4,
          "Tone": 2,
          "Base": 4,
          "Ch_Gate": 0
        },
        {
          "Planet": "Uranus",
          "Lon": 279.5886579062558,
          "Gate": 38,
          "Line": 1,
          "Color": 1,
          "Tone": 4,
          "Base": 3,
          "Ch_Gate": 0
        },
        {
          "Planet": "Neptune",
          "Lon": 284.57379251015533,
          "Gate": 38,
          "Line": 6,
          "Color": 3,
          "Tone": 3,
          "Base": 5,
          "Ch_Gate": 0
        },
        {
          "Planet": "Pluto",
          "Lon": 227.00193884436874,
          "Gate": 1,
          "Line": 5,
          "Color": 1,
          "Tone": 1,
          "Base": 1,
          "Ch_Gate": 0
        }
      ]
    }
  },
  "channels": {
    "Channels": [
      {
        "channel": "30/41: The Channel of Recognition (A Design of Focused Energy)"
      },
      {
        "channel": "7/31: The Channel of the Alpha (A Design of Leadership for 'Good' or 'Bad')"
      }
    ]
  }
}
```

## API Documentation

The project includes an OpenAPI 3.0 specification file named `openapi.yaml`. This file describes the API endpoints, request parameters, responses, and schemas in a standard format.

### Using `openapi.yaml`

You can use the `openapi.yaml` file to:

1.  **Visualize the API**:
    *   **VS Code**: Install extensions like "Swagger Viewer" or "OpenAPI (Swagger) Editor" to preview the API documentation directly in your editor.
    *   **Online Viewers**: Copy the content of `openapi.yaml` and paste it into the [Swagger Editor](https://editor.swagger.io/) to view and interact with the API documentation.

2.  **Import into Postman**:
    *   Open Postman.
    *   Click on the **Import** button in the top left corner.
    *   Drag and drop the `openapi.yaml` file or select it from your file system.
    *   Postman will automatically generate a collection with the request (including examples) pre-configured.

3.  **Generate Client Libraries**:
    *   Tools like `openapi-generator` can use this file to generate API client code for various programming languages (e.g., Python, JavaScript, Java).

