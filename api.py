from fastapi import FastAPI
import tomllib
import os
from routers import general, transits, composite

# --- Read version from pyproject.toml ---
try:
    with open(os.path.join(os.path.dirname(__file__), "pyproject.toml"), "rb") as f:
        project_data = tomllib.load(f)
        __version__ = project_data["project"]["version"]
except FileNotFoundError:
    __version__ = "0.0.0"

app = FastAPI(title="Human Design API", version=__version__)

# Include Routers
app.include_router(general.router)
app.include_router(transits.router)
app.include_router(composite.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
