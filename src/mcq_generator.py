from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
import json, re, os

load_dotenv()

def get_llm(model="mistralai/Mistral-7B-Instruct-v0.2"):
    llm = ChatOpenAI(
        model="gpt-4o-mini",          # or gpt-4-turbo, gpt-3.5-turbo
        temperature=0.6,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )
    return llm

MCQ_PROMPT = """
You are an assistant that generates **one multiple-choice question** (MCQ) for learners age 14-19.
Return output ONLY as JSON with keys: question, choices (list of 4 strings), answer_index (0-3), explanation, difficulty_score (1-10).

Input details:
- subject: {subject}
- difficulty: {difficulty}   # one of: easy, medium, hard
- topic: {topic}  # specific topic within subject
- avoid repeating or rephrasing these previous questions: {past_questions}

Constraints:
- Make options plausible and similar-length.
- Exactly 4 choices.
- answer_index must point to the correct choice.
- difficulty_score: integer 1 (very easy) to 10 (very hard).
- Keep question short (<= 30 words).

Generate 1 question now.
"""

def generate_mcq(subject, difficulty="easy", past_questions=None, topic="General"):
    past_questions = past_questions or []
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(MCQ_PROMPT)
    parser = StrOutputParser()
    chain = prompt | llm | parser
    past_text = ", ".join(past_questions[-10:])
    resp = chain.invoke({"subject": subject, "difficulty": difficulty, "past_questions": past_text, "topic": topic})

    try:
        data = json.loads(resp)
    except Exception:
        import re
        j = re.search(r'\{.*\}', resp, re.DOTALL)
        if j:
            data = json.loads(j.group())
        else:
            raise ValueError("Failed to parse JSON from LLM response")
    return data