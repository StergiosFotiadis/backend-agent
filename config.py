import os

if not os.environ.get("ANTHROPIC_API_KEY"):
    raise EnvironmentError("ANTHROPIC_API_KEY is not set. Add it to your .env file.")

MODEL_NAME = "claude-sonnet-4-6"
TEMPERATURE = 0
MAX_RETRIES = 3

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = "TechFlow-Labs/techflowlabs-knowledge"
SKILLS_GITHUB_PATH = "Software Dev/Projects/Wedding Plan"
