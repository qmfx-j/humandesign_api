import os
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

# --- Load environment variables ---
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path, override=True)

TOKEN = os.getenv("HD_API_TOKEN")
if not TOKEN:
    raise RuntimeError("HD_API_TOKEN environment variable is not set. Please set it before running the API or add it to your .env file.")

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing authentication token.")
    return True
