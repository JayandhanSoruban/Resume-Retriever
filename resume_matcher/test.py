# test_env.py
from dotenv import load_dotenv
import os

env_path = "D:/AGENTIC AI/Resume Retrieval/.env"
print("[DEBUG] .env exists:", os.path.exists(env_path))
load_dotenv(dotenv_path=env_path)
print("[DEBUG] GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))