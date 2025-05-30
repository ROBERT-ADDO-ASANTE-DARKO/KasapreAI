# Can be empty, or you can define package-level imports
from .main import app  # Makes the app available at package level

__all__ = ["app"]  # Controls what gets imported with `from app import
