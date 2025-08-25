import os
from dotenv import load_dotenv
load_dotenv()
OPENROUTER_API_KEY = str(os.getenv("OPENROUTER_API_KEY", ""))
SECRET_KEY=str(os.getenv("SECRET_KEY", ""))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
ALGORITHM=os.getenv("ALGORITHM", "")
