# JCode

Light weight autonomous coding agent built in Python using the Gemini API.

JCode can:
* Inspect project files and directories
* Read and write code
* Executre Python programs inside a sandboxed working directory
* Use structured tool/function calling through Gemini
* Iteratively modify projects based on user prompts

## Example

![JCode Demo](media/example.gif)

## Tech Stack

* Python
    * os
    * argparse
    * dotenv
    * subprocess
* Gemini API
* UV

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

### Architecture Flow (main.py essentially)

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

## Repository Layout

This repository contains both the core JCode agent and several sandbox files generated while testing the agent.

### Core Agent Files
* `main.py` 
    * Handles the conversation loop and Gemini API calls.
* `prompts.py` 
    * Stores the <i>system prompt</i> that defines the agent's behaviour.
* `config.py` 
    * Stores the working directory and any other shared constants.
* `call_function.py` 
    * Maps model-requested functions to actual functions, calling them and returning their value.
* `functions/` 
    * Contains the actual tool implementations .exposed to the model

### Sandbox / Test Files
* `calculator/`
    * Practice project used while testing file reading, writing, and execution.
* `todo/`
    * CLI todo app generate by JCode during testing.
* `lorem.txt`
    * Large sample file used to test `get_file_content.py`
* `test_*.py`
    * Test scripts for individual agent tools.

## Safety Model

All filesystem tools resolve requested paths against a configured working directory within config.py before performing any actions.

This prevents the agent from reading, writing, or executing files outside its allowed sandbox.
