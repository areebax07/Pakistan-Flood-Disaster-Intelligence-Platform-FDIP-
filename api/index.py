import os
import sys

# Add your backend directory to the system path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
)

# Import your Flask app instance from backend/app.py
from app import app