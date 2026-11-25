"""
main.py

A minimal LangChain program that:
  1. Sends a prompt to an OpenAI chat model via LangChain (never calls the
     OpenAI API directly).
  2. Prints the model's response to the terminal.
  3. Enables LangSmith tracing so the run (input, output, timing) shows up
     in your LangSmith project dashboard.

All secrets are read from environment variables. Nothing is hard-coded.

Required environment variables:
  OPENAI_API_KEY        Your OpenAI API key.
  LANGSMITH_API_KEY     Your LangSmith API key.

Optional environment variables (sensible defaults are used if unset):
  OPENAI_MODEL           Chat model name.            default: gpt-4o-mini
  LANGSMITH_PROJECT       LangSmith project name.     default: langchain-demo
  LANGSMITH_TRACING       "true" to enable tracing.   default: true
  LANGSMITH_ENDPOINT      LangSmith API endpoint.     default: https://api.smith.langchain.com

See README.md for setup instructions.
"""

import os
import sys

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load variables from a .env file in the current directory (if present)
# into the process environment. This does NOT override variables that are
# already set in the shell, so `export`-ed values still take priority.
load_dotenv()


def configure_langsmith() -> None:
    """
    Turn on LangSmith tracing using environment variables only.

    LangChain's tracing integration is driven entirely by environment
    variables, so this function just makes sure sane defaults are in place
    without ever hard-coding a key. If LANGSMITH_API_KEY is missing, we
    warn and continue -- tracing will simply be skipped by LangChain.
    """
    if not os.environ.get("LANGSMITH_API_KEY"):
        print(
            "[warning] LANGSMITH_API_KEY is not set. The script will still "
            "call OpenAI, but no trace will be sent to LangSmith.",
            file=sys.stderr,
        )
        return

    # Only set these if the user hasn't already configured them themselves.
    os.environ.setdefault("LANGSMITH_TRACING", "true")
    os.environ.setdefault("LANGSMITH_PROJECT", "langchain-demo")
    os.environ.setdefault("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")


def build_llm() -> ChatOpenAI:
    """Construct the LangChain chat model wrapper around OpenAI."""
    if not os.environ.get("OPENAI_API_KEY"):
        print(
            "[error] OPENAI_API_KEY is not set. Export it before running "
            "this script.",
            file=sys.stderr,
        )
        sys.exit(1)

    model_name = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    # ChatOpenAI reads OPENAI_API_KEY from the environment automatically,
    # so we never pass a key directly in code.
    return ChatOpenAI(model=model_name, temperature=0.7)


def run(prompt: str) -> str:
    """Send `prompt` to the model through LangChain and return the reply text."""
    llm = build_llm()

    messages = [
        SystemMessage(content="You are a helpful, concise assistant."),
        HumanMessage(content=prompt),
    ]

    response = llm.invoke(messages)
    return response.content


def main() -> None:
    configure_langsmith()

    print("LangChain + OpenAI chat (type 'exit' or 'quit' to stop)\n")

    while True:
        try:
            prompt = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not prompt:
            continue
        if prompt.lower() in ("exit", "quit"):
            print("Exiting.")
            break

        answer = run(prompt)

        print("\nModel response:")
        print("-" * 60)
        print(answer)
        print("-" * 60)

        if os.environ.get("LANGSMITH_API_KEY"):
            project = os.environ.get("LANGSMITH_PROJECT", "langchain-demo")
            print(
                f"Trace sent to LangSmith project '{project}'. "
                "Check https://smith.langchain.com to view input, output, and timing.\n"
            )
        else:
            print()


if __name__ == "__main__":
    main()