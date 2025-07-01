from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

load_dotenv()


@tool
def multiply(x: float, y: float) -> float:
    """Multiply 'x' times 'y'."""
    return x * y


if __name__ == "__main__":
    print("Hello Tool Calling")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "you're a helpful assistant"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    # Prebuilt search tool & 1 custom multiply tool
    tools = [TavilySearch(), multiply]
    # llm = ChatOpenAI(model="gpt-4-turbo")
    llm = ChatOllama(model="llama3.1", temperature=0)

    # create a function calling agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    # res = agent_executor.invoke(
    #     {
    #         "input": "what is the weather in dubai right now? compare it with San Fransisco, output should in in celsius",
    #     }
    # )
    # {'input': 'what is the weather in dubai right now? compare it with San Fransisco, output should in in celsius', 'output': 'The current weather in Dubai is clear skies with a temperature of 34°C (93°F) on Tuesday and Wednesday. In San Francisco, the weather is scattered clouds with a temperature of 17°C (63°F) on Tuesday and light rain with a temperature of 74°F (23°C) on Wednesday.\n\nNote: The temperatures are in Celsius as requested by the user.'}

    res = agent_executor.invoke(
        {
            "input": "what is the weather in Singapore right now? compare it with Taipei, output should in in celsius",
        }
    )
    # {'input': 'what is the weather in Singapore right now? compare it with Taipei, output should in in celsius', 'output': 'The current weather in Singapore is:\n\n* Tuesday: light rain, 28°C\n* Wednesday: moderate rain, 30°C\n\nThe current weather in Taipei is:\n\n* Monday: scattered clouds, 35°C\n* Tuesday: sky is clear, 35°C\n* Wednesday: few clouds, 35°C'}

    print(res)
