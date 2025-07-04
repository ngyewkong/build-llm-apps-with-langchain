# build-llm-apps-with-langchain

## Project Setup

- using pipenv as package manager
  - pip3 install pipenv
  - pipenv shell
- install dependencies required
  - pipenv install langchain
  - pipenv install langchain-openai (3rd party for openai models)
  - pipenv install langchain-community (open source community helper packages like text-splitters etc)
  - pipenv install langchainhub
- running with the correct python kernel interpreter
  - cmd + shift + p (and go to Python interpreter)
  - select the interpreter that was created during pipenv shell
- set up .env files to hold credentials/api keys
  - from dotenv import load_dotenv (to pass env variables into code)
- set $PYTHONPATH in shell env (bash or zsh) to include the project workdir
  - so that nested modules/packages can be picked up by vscode during runtime

## Notes

- custom developed packages --> need an empty \_\_init\_\_.py
- name of package dir must be in underscore (third_party not third-party)
- it also need to be on the same dir level as the executing py file by default
  - unless a launch.json is customised in vscode to extend the pythonpath or add in settings.json
  - https://k0nze.dev/posts/python-relative-imports-vscode/

## Agents

- use LLM to reason & process tasks
  - Chain Of Thought Reasoning via Prompt Engineering
- LLMs do not have access to external data that it is not trained on -> agents allow us to connect third party services to interact
- langchain tools allow us to convert python functions into tools which we can allow llm to have access to
- note: use raw gist if not will have JSONDECODEERROR

## MCP Servers

- MCPdoc from langchain (https://github.com/langchain-ai/mcpdoc)
  - retrieve latest documentations from langchain website
- npx @modelcontextprotocol/inspector
  - to test MCP server functionality (ensure the proxy token is copied when MCP Inspector is ran)
    ![MCP Inspector Success Connection to MCP Server Tools](image.png)
- MCP Client
  - Invoke Tools
  - Queries for Resources
  - Interpolates Prompts
- MCP Server
  - Exposes Tools
  - Exposes Resources
  - Exposures Prompts
- Tools (Model Controlled)
  - Functions invoked by the LLM (eg. Search/Retrieve, Send Msg, Update DB)
- Resources (Application Controlled)
  - Data exposed to the application (eg. Files, DB Records, API Responses)
- Prompts (User Controlled)
  - Pre-defined templates for AI Interactions (eg. Doc Q&A, Transcript Summary, JSON Output)
- LangChain's bind_tools
  - Tools bind to LLM
- MCP
  - Tools bind to AI Apps (eg Cursor, windsurf, Claude Desktop, LangGraph Agent etc)
  - MCP Clients are the one who are injecting the instructions of the tools that we need to invoke to the LLM layer
- LangChain's MCP Adapter (https://github.com/langchain-ai/langchain-mcp-adapters)
  - enable seamless integration of MCP tools with LangChain & LangGraph
  - tools capabilitity
- to run mcp servers
  - uv run server_file.py
- Ollama Models not all support tool calling
  - mistral & llama 3.1 supported
