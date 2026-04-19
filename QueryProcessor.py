from embedder import embed_User_query
from vectorstore import search_in_pinecone
from llm import query_llm_with_context
from guardrails import check_input_guardrail, check_output_guardrail
from evaluator import evaluate_rag_response


def process_user_query(query: str) -> dict:
    # 1. Input guardrail — block off-topic or injected queries
    input_check = check_input_guardrail(query)
    if not input_check["allowed"]:
        return {
            "answer": f"I can only help with HR policy questions. {input_check['reason']}",
            "blocked": True,
            "block_reason": input_check["reason"],
            "scores": None
        }

    # 2. Embed and retrieve relevant chunks
    query_vector = embed_User_query(query)
    matched_chunks = search_in_pinecone(query_vector)

    # 3. Build context string and generate answer
    context = "\n\n".join(matched_chunks)
    generated_response = query_llm_with_context(query, context)

    # 4. Output guardrail — ensure answer is grounded in retrieved context
    output_check = check_output_guardrail(generated_response, matched_chunks)
    if not output_check["grounded"]:
        return {
            "answer": "I was unable to generate a reliable answer from the HR policy documents. Please try rephrasing your question.",
            "blocked": True,
            "block_reason": f"Answer not grounded in context: {output_check['reason']}",
            "scores": None
        }

    # 5. Evaluate the response quality
    scores = evaluate_rag_response(query, generated_response, matched_chunks)

    return {
        "answer": generated_response,
        "blocked": False,
        "block_reason": None,
        "scores": scores
    }


if __name__ == "__main__":
    result = process_user_query("What is the leave policy?")
    print("Answer:", result["answer"])
    print("Scores:", result["scores"])
