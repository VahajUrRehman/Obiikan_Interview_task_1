import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()


#Using Hugging Face Inference API
client = InferenceClient(
    provider="sambanova",
    api_key=os.getenv("HF_TOKEN"),
)


def generate_answer(question: str, context: str) -> str:
    print(f"[LLM] Question: {question}, Context: {context}")
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. and You HAve To Answer The Question Only Based On The Context Provided and No Other Source Use If The Context Is Same as question tHEN answer with your wisdom. "
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {"type": "text", "text": context}
            ]
        }
      
    ]
    completion = client.chat.completions.create(
        model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
        messages=messages
    )
    result = completion.choices[0].message["content"]


#  
    print(f"[LLM] Result: {result}")
    return result
