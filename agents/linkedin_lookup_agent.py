# ReAct: Synergizing Reasoning and Acting in Language Models
# Agent Executor is the runtime of the agent
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain import hub  # to access open source prompts
import os
from dotenv import load_dotenv

from tools.tools import get_profile_url_tavily

load_dotenv()


def lookup(name: str) -> str:
    agent_llm = ChatOllama(
        temperature=0,
        model="llama3.1"
    )

    template = """
    Given the full name {name_of_person} I want you to get me a link to their linkedin profile page. 
    Your answer should contain only the linkedin url.
    """

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profile page",  # name the llm going to refer to
            func=get_profile_url_tavily,  # the python function that you want the tool to run
            # description is important for llm (used by llm to determine if they need to use this tool or not)
            description="useful for when you need to get the linkedin page url",
        )
    ]

    # download the React prompt (harrison chase prompt that used for react prompting)
    # prompt that will be sent to the llm (used as the reasoning engine of the agent)
    # this prompt implement the react paper (using chain of thought)
    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=agent_llm, tools=tools_for_agent, prompt=react_prompt
    )

    # provide the agent to the runtime
    # the final agent that you invoke
    # verbose to True to see the logs and understand how the agent is working
    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True
    )

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]

    return linkedin_profile_url


if __name__ == "__main__":
    linkedin_url = lookup(name="Yew Kong NG DBS Bank")
    print(linkedin_url)
