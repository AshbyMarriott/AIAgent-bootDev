import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from prompts import system_prompt
from config import model_name
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)


    if len(sys.argv) < 2:
        raise Exception('Usage: uv run main.py "[your input prompt]"')
        return 1

    verbose = False
    if '--verbose' in sys.argv:
        verbose = True

    prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    response = client.models.generate_content(
        model=model_name,
        contents = messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
    
    if verbose:
        print(f"User prompt: {prompt}")
        prompt_tokens = response.usage_metadata.prompt_token_count
        candidates_token_count = response.usage_metadata.candidates_token_count
        print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {candidates_token_count}")

    if response.function_calls == None:
        print(response.text)
    else:
        for funcCall in response.function_calls:
            #print(f'Calling function: {funcCall.name}({funcCall.args})')
            result = call_function(types.FunctionCall(
                name=funcCall.name,
                args=funcCall.args
                ),
                verbose)
            if result.parts[0].function_response.response == None:
                raise Exception(f"Fatal error: no response from {funcCall.name}")
            elif '--verbose' in sys.argv:
                print(f"-> {result.parts[0].function_response.response}")

    
    

if __name__ == "__main__":
    main()
