import os
from pathlib import Path

from dotenv import load_dotenv


# Always load from backend/.env first, regardless of run directory.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_ROOT / ".env")
load_dotenv()

GEMINI_MODEL_NAME = "gemini-2.5-flash"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

DEFAULT_COMPANY_PROFILE = "NBFC providing digital lending services in India"

DEFAULT_REGULATION_TEXT = (
    "RBI Digital Lending Guidelines Amendment #3:\n"
    "- Loan limit increased to Rs 10,00,000\n"
    "- Mandatory video KYC above Rs 2,00,000\n"
    "- Interest cap reduced to 21%"
)

DEFAULT_COMPANY_POLICY = (
    "Current system supports loan limit Rs 5,00,000\n"
    "No video KYC implemented\n"
    "Interest rate fixed at 24%"
)
