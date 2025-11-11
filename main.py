import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt

def main():
    load_dotenv()
   
    verbose = "--verbose" in sys.argv
    args = []

    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)])
        ]

    generate_content(client, messages, verbose)

# function to generate the content of the response
# extracted for code organization
def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
        print(response.text)
    
    if not response.function_calls:
        return response.text
    
    function_responses = []

    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        function_call_result = call_function(function_call_part, verbose)

        if function_call_result.parts and function_call_result.parts[0].function_response.response:
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            # will we return this later?
            function_responses.append(function_call_result)
        else:
            raise Exception("Function call was not successful")


if __name__ == "__main__":
    main()
