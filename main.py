import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("api key not found")
    
    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash"
    content = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    generated_content = client.models.generate_content(model=model, contents=content)

    if generated_content.usage_metadata is None:
        raise RuntimeError("api request failed")

    tokens_prompt = generated_content.usage_metadata.prompt_token_count
    tokens_response = generated_content.usage_metadata.candidates_token_count 
    
    print(f"User prompt: {content}")
    print(f"Prompt tokens: {tokens_prompt}")
    print(f"Response tokens: {tokens_response}")
    print("Response:")
    print(generated_content.text)



if __name__ == "__main__":
    main()
