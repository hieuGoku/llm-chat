"""Root constant define."""
import os

MONGO_DETAILS = os.getenv("MONGO_DETAILS")

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ADMIN_USER = -1
SUPER_USERNAME = os.getenv('SUPER_USERNAME')
SUPER_PASSWORD = os.getenv('SUPER_PASSWORD')
