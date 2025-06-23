from tabnanny import verbose
from typing import Any
from dotenv import load_dotenv
from langchain import hub
from langchain_ollama import ChatOllama
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL
from langchain_experimental.agents.agent_toolkits import create_csv_agent

# PythonREPLTool allows agent to write and run python code (dangerous in production)

load_dotenv()


def main():
    print("Hello... Start...")

    instructions = """
        You are an agent designed to write and execute python code to answer questions.
        You have access to a python REPL, which you can use to execute python code.
        If you get an error, debug your code and try again.
        Only use the output of your code to answer the question. 
        You might know the answer without running any code, but you should still run the code to get the answer.
        If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
    """

    base_prompt = hub.pull("langchain-ai/react-agent-template")
    # pass in additional instructions to the base prompt
    prompt = base_prompt.partial(instructions=instructions)

    # create the tool list
    python_repl = PythonREPL()
    repl_tool = Tool(
        name="python_repl",
        description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
        func=python_repl.run,
    )
    tools = [repl_tool]

    # create the agent running python code
    agent = create_react_agent(
        prompt=prompt,
        llm=ChatOllama(temperature=0, model="gemma2"),
        tools=tools
    )

    # intialise the runtime of the python agent
    python_agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True)

    # # invoke python agent with input
    # python_agent_executor.invoke(
    #     input={
    #         "input": """generate and save in current working directory 15 QRcodes
    #                     that point to www.udemy.com/course/langchain, you have qrcode package installed already
    #                 """
    #     }
    # )

    # Thought: I need to generate 15 QR codes that point to the given URL and save them. I can use the `qrcode` package for this.
    # Action: python_repl
    # Action Input: ```python
    # import qrcode

    # url = "https://www.udemy.com/course/langchain"
    # for i in range(15):
    #     qr = qrcode.QRCode(
    #         version=1,
    #         error_correction=qrcode.constants.ERROR_CORRECT_L,
    #         box_size=10,
    #         border=4,
    #     )
    #     qr.add_data(url)
    #     qr.make(fit=True)
    #     img = qr.make_image(fill_color="black", back_color="white")
    #     img_path = f"qrcode_{i+1}.png"
    #     img.save(img_path)
    #     print(f"{img_path} saved")
    #  Python REPL can execute arbitrary code. Use with caution.
    #  qrcode_15.png saved
    #  I have generated 15 QR codes and saved them as qrcode_1.png to qrcode_15.png.
    #  Final Answer: 15 QR codes have been generated and saved in the current working directory.

    # underlying use pandas agent with custom prompt that allows agent to handle pandas and schemas
    csv_agent = create_csv_agent(
        llm=ChatOllama(temperature=0, model="gemma3"),
        path="episode_info.csv",
        verbose=True,
        allow_dangerous_code=True  # needed to opt in to allow arbitrary code run disclaimer
    )

    # # invoke the csv agent
    # csv_agent.invoke(
    #     input={"input": "how many columns are there in file episode_info.csv"}
    # )

    # csv_agent.invoke(
    #     input={
    #         "input": "which writer write the most episodes? How many episodes do he/she write?"
    #     }
    # )

    # The output shows the count of each writer. I need to find the writer with the highest count and the count itself. The writer "Larry David" appears 29 times, which is the highest.
    # Action: python_repl_ast
    # Action Input: `df[df['Writers'] == 'Larry David'].shape[0]`29Final Answer: Larry David writes 29 episodes.
    # the number is actually wrong in this case

    # csv_agent.invoke(
    #     input={
    #         "input": "print the seasons by ascending order of the number of episodes they have"
    #     }
    # )

    # Implementing the Router Agent to route requests to the correct agent to use

    # func to wrap and return the format that langchain base.py expects
    # artificially adds in the input key
    def python_agent_executor_wrapper(original_prompt: str) -> dict[str, Any]:
        return python_agent_executor.invoke({"input": original_prompt})

    route_tools = [
        Tool(
            name="Python Code Gen Agent",
            func=python_agent_executor_wrapper,
            description="""useful when you need to transform natural language to python code and execute the python code,
                            returning the results of the code execution
                            DOES NOT ACCEPT CODE AS INPUT
            """,
        ),
        Tool(
            name="CSV Analysis Agent",
            func=csv_agent.invoke,
            description="""useful when you need to answer questions over episode_info.csv file,
                            takes an input the entire question and returns the answer after running pandas methods.
            """
        )
    ]

    route_prompt = base_prompt.partial(instructions="")
    route_agent = create_react_agent(
        prompt=route_prompt,
        llm=ChatOllama(temperature=0, model="gemma3"),
        tools=route_tools
    )
    route_agent_executor = AgentExecutor(
        agent=route_agent, tools=route_tools, verbose=True)

    print(
        route_agent_executor.invoke(
            {
                "input": "which season has the most episodes?"
            }
        )
    )

    # Thought: Do I need to use a tool? Yes
    # Action: CSV Analysis Agent
    # Action Input: {"question": "which season has the most episodes?"}

    # > Entering new AgentExecutor chain...
    # Thought: I need to count the number of episodes for each season and then find the season with the maximum number of episodes.
    # Action: python_repl_ast
    # Action Input: `df['Season'].value_counts()`Season
    # 4    24
    # 7    24
    # 3    23
    # 6    22
    # 8    22
    # 5    21
    # 9    21
    # 2    12
    # 1     5
    # Name: count, dtype: int64I have the episode counts for each season. Now I need to identify the season with the highest count.
    # Action: python_repl_ast
    # Action Input: `df['Season'].value_counts().idxmax()`4Final Answer: 4

    # > Finished chain.
    # {'input': '{"question": "which season has the most episodes?"}', 'output': '4'}Do I need to use a tool? No
    # Final Answer: Season 4 has the most episodes.

    # > Finished chain.
    # {'input': 'which season has the most episodes?', 'output': 'Season 4 has the most episodes.'}

    print(
        route_agent_executor.invoke(
            {
                "input": """generate and save in current working directory 15 QRcodes that point to www.udemy.com/course/langchain, you have qrcode package installed already
                         """
            }
        )
    )

    # Thought: Do I need to use a tool? Yes
    # Action: Python Code Gen Agent
    # Action Input: ```python
    # import qrcode
    # import os

    # url = "https://www.udemy.com/course/langchain"
    # qr_codes = []
    # for i in range(15):
    #     qr = qrcode.QRCode(
    #         version=1,
    #         error_correction=qrcode.constants.ERROR_CORRECT_L,
    #         box_size=10,
    #         border=4,
    #     )
    #     qr.add_data(url)
    #     qr.make(fit=True)
    #     img = qr.make_image(fill_color="black", back_color="white")
    #     filename = f"qrcode_{i+1}.png"
    #     img.save(filename)
    #     qr_codes.append(filename)

    # print(qr_codes)
    # ```

    # > Entering new AgentExecutor chain...
    # Thought: Do I need to use a tool? No
    # Final Answer:  ['qrcode_1.png', 'qrcode_2.png', 'qrcode_3.png', 'qrcode_4.png', 'qrcode_5.png', 'qrcode_6.png', 'qrcode_7.png', 'qrcode_8.png', 'qrcode_9.png', 'qrcode_10.png', 'qrcode_11.png', 'qrcode_12.png', 'qrcode_13.png', 'qrcode_14.png', 'qrcode_15.png']


if __name__ == "__main__":
    main()
