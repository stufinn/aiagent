import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt
from config import MAX_COUNT

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
    
    count = 0
    while True:
        count += 1
        if count > MAX_COUNT:
            print(f"Maximum iterations ({MAX_COUNT}) reached.")
            sys.exit(1)

        try:
            # A response is only returned if there are no function calls
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


    # generate_content(client, messages, verbose)

# function to generate the content of the response
# extracted for code organization
def generate_content(client, messages, verbose):
    # print("messages", messages)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    # Add the content from each candidate to the message list
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    if not response.function_calls:
        return response.text
    
    function_responses = []

    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)

        if (
            not function_call_result.parts 
            or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")
        
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    
    messages.append(types.Content(role="user", parts=function_responses))


if __name__ == "__main__":
    main()
