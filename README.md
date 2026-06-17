# Python AI Code Agent

An autonomous coding assistant built with Python and the Google Gemini API. This agent can inspect a local directory, read files, write code, and execute Python scripts to debug and solve programming tasks.

## Features

- **Autonomous Debugging**: Analyzes error messages and source code to identify logic flaws.
- **Tool Use**: Utilizes a function-calling loop to interact with the filesystem and a Python interpreter.
- **Context-Aware**: Searches and reads local files to understand the project structure before making changes.
- **Verification**: Can run the code it writes to ensure the "fix" actually works.

## Tech Stack

- **Language**: Python 3.13
- **LLM**: Google Gemini (via `google-generativeai` SDK)
- **Environment**: Decoupled configuration using `python-dotenv`

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package and environment management.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```
2. **Create a virtual environment and install dependencies:**
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install google-generativeai python-dotenv
   ```
3. **Set up environment variables:**

   Create a .env file in the root directory:

   ```bash
   GEMINI_API_KEY=your_actual_api_key_here
   ```
