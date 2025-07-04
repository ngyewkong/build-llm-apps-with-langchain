from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.messages import HumanMessage

import asyncio

load_dotenv()

# setting how the client run the mcp server
stdio_server_params = StdioServerParameters(
    command="python",
    args=["mcp/servers/math_mcp.py"]
)


async def main():
    async with stdio_client(stdio_server_params) as (read, write):
        # mcp ClientSession is doing the heavy lifting of communicating btw client & server
        async with ClientSession(read_stream=read, write_stream=write) as session:
            # after initialisation of the session, client will know the tools, resources that the MCP server exposes
            await session.initialize()
            print("session initialized...")

            # get the list of tools available
            tools = await session.list_tools()
            # Logs: Processing request of type ListToolsRequest

            # this tools is a list of MCP Tool Obj (not compatible with LangChain Tool Obj)
            # will error with ValueError: The first argument must be a string or a callable with a __name__ for tool decorator. Got <class 'tuple'>
            print(tools)
            # tools=[Tool(name='add', title=None, description='Add two numbers'
            # need to wrap the session with load_mcp_tools from Langchain
            tools = await load_mcp_tools(session=session)
            print(tools)
            # [StructuredTool(name='add', description='Add two numbers' which is LangChain Tool Object

            # create the langgraph agent (using MCP host application)
            llm = ChatOllama(model="llama3.1")
            agent = create_react_agent(llm, tools)

            result = await agent.ainvoke({"messages": [HumanMessage(content="What is 2 + 109?")]})
            print(f"Answer is ", result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
