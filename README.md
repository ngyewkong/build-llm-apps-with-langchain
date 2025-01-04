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

## Notes

- custom developed packages --> need an empty \_\_init\_\_.py
- name of package dir must be in underscore (third_party not third-party)
- it also need to be on the same dir level as the executing py file by default
  - unless a launch.json is customised in vscode to extend the pythonpath or add in settings.json
  - https://k0nze.dev/posts/python-relative-imports-vscode/
