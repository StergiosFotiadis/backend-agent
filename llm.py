from langchain_anthropic import ChatAnthropic
from config import MODEL_NAME, TEMPERATURE, MAX_RETRIES

llm = ChatAnthropic(model=MODEL_NAME, temperature=TEMPERATURE, max_retries=MAX_RETRIES)
