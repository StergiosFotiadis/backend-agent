import os

if not os.environ.get("ANTHROPIC_API_KEY"):
    raise EnvironmentError("ANTHROPIC_API_KEY is not set. Add it to your .env file.")

MODEL_NAME = "claude-sonnet-4-6"
TEMPERATURE = 0
MAX_RETRIES = 3

SKILLS_PATH = os.path.join(os.path.dirname(__file__), "skills")
