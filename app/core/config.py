import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables once

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/school_db")
SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecret")  # Example for authentication
