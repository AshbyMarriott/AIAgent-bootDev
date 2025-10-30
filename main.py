import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from prompts import system_prompt
from config import model_name


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)


    if len(sys.argv) < 2:
        raise Exception('Usage: uv run main.py "[your input prompt]"')
        return 1

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    response = client.models.generate_content(
        model=model_name,
        contents = messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
    
    if '--verbose' in sys.argv:
        print(f"User prompt: {prompt}")
        prompt_tokens = response.usage_metadata.prompt_token_count
        candidates_token_count = response.usage_metadata.candidates_token_count
        print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {candidates_token_count}")

    if response.function_calls == []:
        print(response.text)
    else:
        for funcCall in response.function_calls:
            print(f'Calling function: {funcCall.name}({funcCall.args})')

    
    

if __name__ == "__main__":
    main()
