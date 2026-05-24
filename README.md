# JCode

Light weight autonomous coding agent built in Python using the Gemini API.

JCode can:
* Inspect project files and directories
* Read and write code
* Executre Python programs inside a sandboxed working directory
* Use structured tool/function calling through Gemini
* Iteratively modify projects based on user prompts

## Example


## Tech Stack

* Python
* Gemini API
* uv
* argparse
* dotenv

## Current Features

* `get_files_info`
* `get_file_content`
* `write_file`
* `run_python_file`

## How It Works

After sending the user prompt and predefined system prompt found within `prompts.py`, JCode uses Gemini function calling to allow the model to interact with a local codebase through a controlled set of Python tools.

The model does not directly access the filesystem or execute commands on its own. Instead, it receives a list of available tools schemas describing the functions it's allowed to use. Based on the user's request and available tools, Gemini returns structured function call requests back to the application.

Each of the tools available to the agent are implemented inside the `functions/` directory. Once a structured function call is returned by the model, `main.py` passes the request to `call_function.py`, which maps the requested function name to the corresponding real Python function and executes it inside a sandboxed working directory.

After execution, the function result is packaged into a structured tool response and appended back into the conversation history, allowing Gemini to reason about the output, continue iterating, or generate a final natural-language response!

### Core Design
* `main.py` handles the conversation loop and Gemini API calls.
* `prompts.py` stores the <i>system prompt</i> that defines the agent's behaviour.
* `config.py` stores the working directory and any other shared constant.
* `call_function.py` maps model-requested functions to actual functions, calling them and returning their value.
* `functions/` contains the actual tool implementations for reading files, writing to files, listing directories, and running Python code.

### Flow Chart (main.py essentially)

```
User Prompt + System Prompt
↓
Gemini API  <---------------------------
↓                                       \
Model Response Added to Conversation     \
↓                                         |
Function Call Request                     |
↓                                         |
call_function.py Runs Requested Function  /
↓                                        /
Function Response Added to Conversation /
↓
If Model Stops Requesting Function Calls, Agent Loop Breaks
↓
Final Response Printed to Console
```

## Safety Model

All filesystem tools resolve requested paths against a configured working directory within config.py before performing any actions.

This prevents the agent from reading, writing, or executing files outside its allowed sandbox.
