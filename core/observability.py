import os
from dotenv import load_dotenv

load_dotenv()

# Set Opik env vars — SDK reads these automatically, no configure() call needed
os.environ["OPIK_API_KEY"] = os.getenv("COMET_API_KEY", "")
os.environ["OPIK_WORKSPACE"] = os.getenv("COMET_WORKSPACE", "")
os.environ["OPIK_PROJECT_NAME"] = os.getenv("COMET_PROJECT_NAME", "insurance-ai")
