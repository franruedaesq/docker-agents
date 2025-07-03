from api.ai.llms import get_openai_llm
from api.ai.schemas import EmailMessageSchema


def generate_email_message(query: str):
    llm_base = get_openai_llm()
    llm = llm_base.with_structured_output(EmailMessageSchema)

    messages = [
        ("system", "You are a helpful assistant for research and composing plaintext emails. Do not use markdown or HTML formatting."),
        ("human", f"{query}. Do not use markdown in your response only plaintext."),
    ]

    return llm.invoke(messages)