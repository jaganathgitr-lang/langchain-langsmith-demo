# LangChain + LangSmith Demo


A single-file (`main.py`) program that sends a prompt to an OpenAI chat
model **through LangChain** and traces the run in **LangSmith**.

## 1. Set up a clean environment

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install --upgrade pip
```

## 2. Install the libraries

```bash
pip install -r requirements.txt
```

This installs:
- `langchain` and `langchain-openai` — the framework + OpenAI chat model wrapper
- `langsmith` — the tracing client LangChain uses under the hood

## 3. Add your API keys

Get keys from:
- OpenAI: https://platform.openai.com/api-keys
- LangSmith: https://smith.langchain.com/ → Settings → API Keys

Copy the example env file and fill in your real values:

```bash
cp .env.example .env
```

Edit `.env`:

```
OPENAI_API_KEY=sk-...your real key...
LANGSMITH_API_KEY=lsv2_...your real key...
```

`main.py` automatically loads `.env` at startup using `python-dotenv`, so
you don't need to `export` anything manually — just make sure `.env` sits
in the same folder as `main.py` and has real values filled in.

(If you'd rather not rely on `.env` loading, you can still export the
variables in your shell instead: `export $(grep -v '^#' .env | xargs)` —
shell-exported values take priority over `.env` either way.)

`.env` is already listed in `.gitignore` so it won't be committed.

## 4. Run the program

```bash
python main.py "Explain vector databases in two sentences."
```

If you don't pass an argument, it uses a built-in default prompt.

You should see the prompt, then the model's response printed in the
terminal, followed by a confirmation that a trace was sent to LangSmith.

## 5. Confirm the run in LangSmith

1. Go to https://smith.langchain.com
2. Open the project named by `LANGSMITH_PROJECT` (default: `langchain-demo`)
3. You should see a new run listed with:
   - The exact input messages (system + human)
   - The model's output
   - Latency / timing and token usage

## How tracing is enabled

LangChain automatically sends traces to LangSmith when these environment
variables are set — no extra code is needed in `main.py` beyond making
sure they're present:

| Variable            | Purpose                                   |
|----------------------|--------------------------------------------|
| `LANGSMITH_TRACING`  | `"true"` turns tracing on                 |
| `LANGSMITH_API_KEY`  | Authenticates with your LangSmith account |
| `LANGSMITH_PROJECT`  | Which project the runs are grouped under  |
| `LANGSMITH_ENDPOINT` | API endpoint (defaults to the public one) |

`main.py` sets defaults for the non-secret values only if they aren't
already set, and never hard-codes either API key — both are read strictly
from the environment.

## Notes

- Swap the model by setting `OPENAI_MODEL` (e.g. `gpt-4o`, `gpt-4.1-mini`).
- If `LANGSMITH_API_KEY` is unset, the script still runs and calls OpenAI,
  it just skips tracing and prints a warning.
- If `OPENAI_API_KEY` is unset, the script exits with an error before
  making any network call.
## Tech stack
Python · LangChain · OpenAI · LangSmith · python-dotenv
