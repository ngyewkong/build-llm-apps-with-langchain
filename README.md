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
<<<<<<< HEAD
- set $PYTHONPATH in shell env (bash or zsh) to include the project workdir
  - so that nested modules/packages can be picked up by vscode during runtime
=======
>>>>>>> 50c7328 (refactor ice_breaker & add third_party package for linkedin profile scrapping)

## Notes

- custom developed packages --> need an empty \_\_init\_\_.py
- name of package dir must be in underscore (third_party not third-party)
- it also need to be on the same dir level as the executing py file by default
  - unless a launch.json is customised in vscode to extend the pythonpath or add in settings.json
  - https://k0nze.dev/posts/python-relative-imports-vscode/
<<<<<<< HEAD

## Agents

- use LLM to reason & process tasks
  - Chain Of Thought Reasoning via Prompt Engineering
- LLMs do not have access to external data that it is not trained on -> agents allow us to connect third party services to interact
- langchain tools allow us to convert python functions into tools which we can allow llm to have access to
- note: use raw gist if not will have JSONDECODEERROR
=======
>>>>>>> 50c7328 (refactor ice_breaker & add third_party package for linkedin profile scrapping)
