# using langchain impl of MCPClient to handle multiple MCP servers connections
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

llm = ChatOllama(model="llama3.1")


async def main():
    print("Hello langchain MCP")
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": [
                    "mcp/servers/math_mcp.py"
                ],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    )
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)
    result = await agent.ainvoke({"messages": "What is 2 + 2?"})
    # result = await agent.ainvoke(
    #     {"messages": "What is the weather in San Francisco?"}
    # )

    print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
