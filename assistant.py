from starter import rag
import math


input_tokens = []

for i in range(4):
    query = "How does the agentic loop keep calling the model until it stops?"
    response = rag.rag(query)
    answer = response.output_text
    input_tokens.append(rag.input_tokens)


print(f"Minimum tokens: {min(input_tokens)}")
print(f"Maximum tokens: {max(input_tokens)}")
print(f"Max variance: {max(input_tokens)/min(input_tokens)}")






