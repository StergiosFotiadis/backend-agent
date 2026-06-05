from langchain_core.prompts import ChatPromptTemplate

router_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a request classifier for a backend developer agent.

Classify the user request into exactly one of these routes:
- generate: user wants to create or modify code (new endpoint, feature, schema, model, etc.)
- plan: user wants to understand what would be built, without generating code
- review: user wants existing code reviewed for security or quality issues

Reply with only one word: generate, plan, or review.""",
    ),
    ("human", "{request}"),
])
