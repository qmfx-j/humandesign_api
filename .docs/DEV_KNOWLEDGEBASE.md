# Developer Knowledge Base & Troubleshooting

This document serves as a repository for technical challenges encountered during development and their specific solutions.


## Data Handling & Serialization

### 1. JSON Serialization of NumPy Types
**Symptom:**
- `TypeError: Object of type int64 is not JSON serializable` when trying to dump Human Design calculation results to JSON.

**Cause:**
- `pandas` and `numpy` operations often return numpy scalar types (`np.int64`, `np.float64`) instead of native Python types. The standard `json` library does not know how to handle these.

**Solution:**
- Implement a custom `json.JSONEncoder` subclass that checks for `np.integer`, `np.floating`, and `np.ndarray` and converts them to their Python equivalents (`int`, `float`, `list`).
- Pass this encoder class to `json.dumps(..., cls=NumpyEncoder)`.


## API Usage & Validation

### 2. Flexible API Inputs (String/Integer Coercion)
**Symptom:**
- Clients sending dates as strings (e.g., `"year": "1990"`) or numbers with leading zeros (e.g., `"minute": "00"`) might fear compatibility issues.

**Solution:**
- The API uses Pydantic `validator` with `pre=True` to intercept inputs before validation.
- It automatically coerces strings to integers (`"00"` -> `0`, `"1990"` -> `1990`).
- This allows flexible integration with various client configurations.

### 3. JSON Syntax: Leading Zeros
**Symptom:**
- `422 Unprocessable Entity` or `JSON decode error` when sending `"minute": 00` (unquoted).

**Cause:**
- The JSON standard **prohibits** leading zeros for numbers. `00` is not valid JSON. `0` is valid.

**Solution:**
- **Client-side:** Send valid integers (`0`) or quoted strings (`"00"`).
- **Server-side:** The API is configured to accept the quoted string `"00"` and convert it to integer `0`.

## Algorithmic Logic

### 4. Human Design Definition Calculation
**Symptom:**
- Charts with cyclic definition (e.g., Head-Ajna connected, Throat-Sacral connected, but independent) were incorrectly identified as "Reflector" (0 splits) or "Single Definition".

**Cause:**
- Previous logic relied on `len(defined_centers) - len(channels)`. This formula fails for cyclic graphs where islands (connected components) exist but the node/edge count doesn't reflect connectivity.

**Solution:**
- Implemented **Graph Traversal (Depth-First Search)**.
- Build an adjacency list of defined centers based on active channels.
- Traverse the graph to count distinct connected components ("islands").
- **1 Island**: Single Definition.
- **2 Islands**: Split Definition.
- **3 Islands**: Triple Split.
- **4 Islands**: Quad Split.
- **0 Islands (No channels)**: Reflector / No Definition.

## DevOps & Deployment

### 5. Docker Image Size Optimization
**Symptom:**
- The Docker image size was unnecessarily large (~552MB), containing build artifacts and cache.

**Cause:**
- `pip install` in the same layer as the runtime, and lack of `.dockerignore` pruning.

**Solution:**
- **Multi-Stage Build**: Use `pip install --prefix=/install` in a builder stage, then `COPY` only that folder to the final runtime image. This discards the pip cache and build tools.
- **Strict .dockerignore**: Exclude `.git`, `venv`, `__pycache__`, and docs.
- **Result**: Reduced image size by ~19% (to ~447MB).

## Release Notes & History

### Version 1.2.1 (2025-12-22)
- **Transition to Standard Versioning**: Moved the Single Source of Truth for the project version from a custom `version.py` file to the standard `pyproject.toml`.
- **Reasoning**: This aligns with modern Python packaging standards (PEP 621) and simplifies build tool integration.
- **Implementation**: The `api.py` now uses Python 3.11+'s built-in `tomllib` to parse the version at runtime.
### Version 1.2.4 (2025-12-22)
- **API Field Renaming**: Renamed the output field `split` to `definition` to align with domain-specific terminology. This affects all endpoints returning Human Design metrics.
- **Bug Fix**: Corrected a variable shadowing issue in `hd_features.py` that caused a `TypeError` when calculating definition types.
