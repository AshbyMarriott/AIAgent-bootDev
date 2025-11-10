import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from prompts import system_prompt
from config import model_name
from call_function import available_functions, call_function
import time


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
    
    for i in range(1, 20):
        try:    
            response = client.models.generate_content(
                model=model_name,
                contents = messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
            
            if verbose:
                print(f"User prompt: {prompt}")
                prompt_tokens = response.usage_metadata.prompt_token_count
                candidates_token_count = response.usage_metadata.candidates_token_count
                print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {candidates_token_count}")

            for candidate in response.candidates:
                messages.append(candidate.content)
            
            if response.function_calls:
                for funcCall in response.function_calls:
                    
                    result = call_function(types.FunctionCall(
                        name=funcCall.name,
                        args=funcCall.args
                        ),
                        verbose)
                    if result.parts[0].function_response.response == None:
                        raise Exception(f"Fatal error: no response from {funcCall.name}")
                    elif '--verbose' in sys.argv:
                        print(f"-> {result.parts[0].function_response.response}")
                    func_response_message = types.Content(
                        parts=[types.Part(function_response= types.FunctionResponse(
                            name=funcCall.name,
                            response=result.parts[0].function_response.response))],
                        role="user"
                        )
                    messages.append(func_response_message)
                    

            has_calls = any(getattr(c, "function_calls", None) for c in response.candidates) or bool(response.function_calls)
            if not has_calls and response.text:
                print(f'Final Response:\n{response.text}')
                break
            
        except Exception as e:
            if getattr(e, "status", None) == 'RESOURCE_EXHAUSTED':
                print(f'Exception: {e}\nWaiting 2 seconds...')
                time.sleep(2)
                print('Wait finished, continuing')
                continue
            else:
                print(f'Exception: {e}\nExiting')
                return 

    
    

if __name__ == "__main__":
    main()
