from typing import List, Union
from dotenv import load_dotenv
from langchain.agents import tool
from langchain.agents.output_parsers.react_single_input import ReActSingleInputOutputParser
from langchain.tools.render import render_text_description
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain.schema import AgentAction, AgentFinish
from textwrap import dedent

from callbacks import AgentCallbackHandler

load_dotenv()

# description is impt for the llm agent to decide if they need to call this tool or not
# tool decorator is langchain utility function which will take a function and create a langchain tool
# this converts the function to a StructuredTool --> mean we cannot run or invoke the function like normal function call
# need to use the .invoke method to invoke directly that take a dictionary as input instead


@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length enter with {text=}")

    # removing non alphabetic characters
    text = text.strip("'\n").strip('"')
    return len(text)


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(
        f"Tool Name not found in List of Tools made available to the LLM")


if __name__ == "__main__":
    print("Hello ReAct LangChain...")
    # print(get_text_length("test"))
    # print(get_text_length.invoke(input={"text": "test"}))
    # create a list of tools to parse to LLM Agent
    tools = [get_text_length]

    # the prompt that is going to help the LLM with tool decision
    template = dedent(
        """\
        Answer the following questions as best you can. You have access to the following tools:

        {tools}

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Begin!

        Question: {input}
        Thought: {agent_scratchpad}\
    """
    )

    # .partial will populate and plug in the values of the placeholders we alr have or know
    # we cannot pass in the tools as is as tools is a langchain tool object but the llm only recognise text as input
    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools), tool_names=",".join(t.name for t in tools)
    )

    # reasoning engine
    # stop -> tell the LLM to stop generating once \nObservation is generated
    # \nObservation as the stop signal as observation shld come from running the tool not from the LLM (if so is hallucination)
    llm = ChatOllama(
        temperature=0,
        # model="deepseek-r1",
        model="mistral",
        stop=["\nObservation"],
        callbacks=[AgentCallbackHandler()]  # instantiate the class
    )

    # keep track of the history of the agent
    intermediate_steps = []

    # create agent using LCEL
    # passing in input as a dict to the prompt (tools & tools_name placeholder are partially filled earlier)
    # setting the value of the input dictionary to be dynamic using lambda function which will be done when agent.invoke()
    # ReActSingleInputOutputParser is using regex to find and search for the corresponding thought action action input
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: x["agent_scratchpad"]
        }
        | prompt
        | llm
        | ReActSingleInputOutputParser()
    )

    agent_step = ""
    while not isinstance(agent_step, AgentFinish):
        # not getting AgentFinish when using ollama (preferably use OpenAI or GCP models)
        agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
            {
                "input": "What is the length in characters for the text TOTHEMOON?",
                "agent_scratchpad": intermediate_steps
            })
        print(f"response: {agent_step}\n")

        if isinstance(agent_step, AgentAction):
            # find the tool name if AgentAction is returned
            tool_name = agent_step.tool
            tool_to_use = find_tool_by_name(tools, tool_name)
            tool_input = agent_step.tool_input

            observation = tool_to_use.func(str(tool_input))
            print(f"Observation: {observation}\n")
            # to add the history after each cycle (both the reasoning history & the action chosen)
            intermediate_steps.append((agent_step, str(observation)))
            print(f"Intermediate Steps: {intermediate_steps}\n")

    if isinstance(agent_step, AgentFinish):
        print(agent_step.return_values)
