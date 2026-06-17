import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("api key not found")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash"
    content = args.user_prompt

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=content)])
    ]

    response = client.models.generate_content(
        model=model, 
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0,
            tools=[available_functions]
        )
    )

    if response.usage_metadata is None:
        raise RuntimeError("api request failed")

    tokens_prompt = response.usage_metadata.prompt_token_count
    tokens_response = response.usage_metadata.candidates_token_count 

    if args.verbose:
        print(f"User prompt: {content}")
        print(f"Prompt tokens: {tokens_prompt}")
        print(f"Response tokens: {tokens_response}")

    if not response.function_calls:
        print("Response:")
        print(response.text)
        return

    function_results = []
    for function_call in response.function_calls:
        # print(f"Calling function: {function_call.name}({function_call.args})")
        function_call_result = call_function(function_call, args.verbose)

        if not function_call_result.parts:
            raise Exception("Empty parts list")
        
        if not function_call_result.parts[0].function_response:
            raise Exception("Not a FunctionResponse object")
        
        if not function_call_result.parts[0].function_response.response:
            raise Exception("Not a function result")
        
        function_results.append(function_call_result.parts[0])

        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")


if __name__ == "__main__":
    main()
