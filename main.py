import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
import sys

def main():
    # load in api key from .env file
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("no api key found")

    # generate ai client
    client = genai.Client(api_key=api_key)
    
    # collect user input
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", 
                        type=str, 
                        help="User prompt")
    parser.add_argument("--verbose", 
                        action="store_true", 
                        help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # agent loop
    for _ in range(20):
        # collect response
        response = generate_response(messages, client)

        if response.usage_metadata == None:
            raise RuntimeError("failed api request")

        # append 
        for candidate in response.candidates:
            messages.append(candidate.content)

        # call the functions
        function_responses = collect_function_call_responses(response, args)

        # break out loop if no function_responses
        if not function_responses:
            break

        # append function results to messages list
        messages.append(types.Content(role="user", parts=function_responses))

    # max iterations reached, but no final response
    else:
        print("Max iterations ran without reaching a final response.")
        sys.exit(1)

    # output
    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")    
    print(f"Response:\n{response.text}")

def collect_function_call_responses(response, args):
    function_results = []

    if response.function_calls:
        for function_call in response.function_calls:
            # call function
            function_call_result = call_function(function_call, args.verbose)

            # error checking
            if not function_call_result.parts:
                raise Exception("missing .parts list")
            if not function_call_result.parts[0].function_response:
                raise Exception("no function response found")
            if not function_call_result.parts[0].function_response.response:
                raise Exception("no response to function response found")

            # append function call response to a list of function results
            function_results.append(function_call_result.parts[0])

            # verbose
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
                
    return function_results


def generate_response(messages, client):
    return client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )

if __name__ == "__main__":
    main()
