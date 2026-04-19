from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from typing import List

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def evaluate_rag_response(query: str, answer: str, context_chunks: List[str]) -> dict:
    """
    Scores the RAG response on 3 metrics using LLM-as-judge (0.0 to 1.0):

    - faithfulness:       Is the answer grounded in the retrieved context?
    - answer_relevancy:   Does the answer directly address the user's question?
    - context_relevancy:  Are the retrieved chunks relevant to the question?
    """
    context = "\n---\n".join(context_chunks)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """You are an evaluation judge for a RAG (Retrieval Augmented Generation) HR assistant.
Score each metric from 0.0 to 1.0:

1. faithfulness: Does the answer contain ONLY information supported by the context?
   1.0 = fully grounded in context, 0.0 = completely hallucinated

2. answer_relevancy: Does the answer directly address the user's question?
   1.0 = perfectly answers the question, 0.0 = completely off-topic

3. context_relevancy: Do the retrieved context chunks contain information needed to answer the question?
   1.0 = context is highly relevant, 0.0 = context is completely irrelevant

Return a JSON object with keys: faithfulness, answer_relevancy, context_relevancy"""
            },
            {
                "role": "user",
                "content": f"Question: {query}\n\nContext:\n{context}\n\nAnswer:\n{answer}"
            }
        ],
        temperature=0
    )

    try:
        raw = response.choices[0].message.content.strip()
        # Strip markdown fences if present (e.g. ```json ... ```)
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        scores = json.loads(raw)
        return {k: round(max(0.0, min(1.0, float(v))), 2) for k, v in scores.items()}
    except Exception:
        return {"faithfulness": 0.0, "answer_relevancy": 0.0, "context_relevancy": 0.0}
