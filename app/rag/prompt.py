from langchain_core.prompts import ChatPromptTemplate

# Template for guiding the LLM to use only provided context
_PROMPT_TEMPLATE = """You're a healthcare policy assistant. Use ONLY the provided context to answer the question.
If unsure, reply: “I couldn't find specific information in the policies”.

Context:
{context}

Question:
{question}

Answer in 1-3 concise sentences. Highlight critical details like coverage limits or deadlines in **bold**.
"""

def get_prompt_template() -> ChatPromptTemplate:
    """
    Returns a ChatPromptTemplate built from the standard healthcare policy prompt.
    """
    return ChatPromptTemplate.from_template(_PROMPT_TEMPLATE)
