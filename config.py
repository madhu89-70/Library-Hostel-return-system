import os
from pathlib import Path
from dotenv import load_dotenv

base_dir = Path(__file__).resolve().parent
env_path = base_dir / '.env'

class Config:
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000")
    LIBRARY_EXIT_ENDPOINT = os.getenv("LIB_ENDPOINT", f"{API_BASE_URL}/scan_library")
    HOSTEL_ENTRY_ENDPOINT = os.getenv("HOSTEL_ENDPOINT", f"{API_BASE_URL}/scan_hostel")