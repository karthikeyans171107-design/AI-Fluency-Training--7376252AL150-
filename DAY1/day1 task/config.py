"""Shared configuration: chooses the LLM provider and holds the lab data."""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # reads the .env file in this folder

PROVIDER = os.getenv("PROVIDER", "ollama").strip().lower()

if PROVIDER == "ollama":                          # Option A: local model, no key
    BASE_URL = "http://localhost:11434/v1"
    API_KEY = "ollama"                             # any text works for Ollama
    MODEL = os.getenv("MODEL", "qwen2.5:1.5b")
elif PROVIDER == "groq":                           # Option B: free cloud key
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")
elif PROVIDER == "huggingface":                    # Option C: free cloud key
    BASE_URL = "https://router.huggingface.co/v1"
    API_KEY = os.getenv("HF_TOKEN")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")
else:
    raise SystemExit(f"Unknown PROVIDER '{PROVIDER}'. Use ollama, groq or huggingface.")

if not API_KEY:
    raise SystemExit(f"No API key found for PROVIDER={PROVIDER}. Check your .env file.")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# Private HR data that no public LLM has ever seen
LEAVE_BALANCE = {"EMP101": 12, "EMP102": 8, "EMP103": 15}  # remaining leave days

QUESTIONS = [
    "How many leave days does EMP102 have left?",
    "What is the total leave balance for EMP101 and EMP103 combined?",
    "Does EMP101 have more leave than EMP102, and by how many days?",
    "Write a two-line reminder message for employees to plan their leave.",
]


def banner(system_name):
    print(f"\n=== {system_name} | provider: {PROVIDER} | model: {MODEL} ===\n")