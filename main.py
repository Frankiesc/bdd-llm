import os
import argparse
import prompts
from sys import exit
from dotenv import load_dotenv
from openai import OpenAI

from config import MAX_LOOPS
from call_function import available_functions, call_function


load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("Could not find OPENROUTER_API_KEY")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# Parses through the cli arguments
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages = []

def call_agent() -> bool:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions
    )

    verbose = args.verbose
    message = response.choices[0].message
    agent_response = message.content
    tool_calls = message.tool_calls

    if not response.usage:
            raise RuntimeError("API response appears to be malformed")

    # Save agent response to history for context
    messages.append(message)

    if verbose:
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)

    if not tool_calls:
        print("Agent:")
        print(agent_response)
        return True

    for tool_call in tool_calls:
        if tool_call.type != "function":
            continue
        result_message = call_function(tool_call, verbose)
        if not result_message.get("content"):
            raise RuntimeError(f"Empty function response for {tool_call.function.name}")

        # Save tool call result to history for context
        messages.append(result_message)
        if verbose:
            print(f"-> {result_message['content']}")
    return False


def main():
    print("Hello from bdd-llm!")

    messages.append( {
        "role": "system",
        "content": prompts.system_prompt
    })

    messages.append( {
        "role": "user",
        "content": args.user_prompt,
    })

    for i in range(MAX_LOOPS):
        if call_agent():
            return

    print("The agent was unable to resolve the request in the specified max amount of loops.")
    exit(1)

if __name__ == "__main__":
    main()
