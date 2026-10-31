import os

from dotenv import load_dotenv

load_dotenv()
from typing import List

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field
from tavily import TavilyClient

# tavily_client = TavilyClient()
# @tool
# def search(query: str) -> str:
#     """
#     Tool that searches over internet
#     Args:
#         query (str): The search query
#     Returns:
#         str: The search results
#     """
#     print(f"Search results for '{query}'")
#     return tavily_client.search(query=query)


class Source(BaseModel):
    """Scheme for a source used by agent"""

    url: str = Field(description="The URL of the source")


class AgentResponse(BaseModel):
    """Scheme for the agent response with answer sources"""

    answer: str = Field(description="The answer from the agent")
    sources: List[Source] = Field(
        default_factory=list, description="The sources used by the agent"
    )


llm = ChatOllama(model="qwen2.5:latest", temperature=0)
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)


def main() -> None:
    print("Hello from langchain-course!")
    result = agent.invoke(
        {
            "messages": HumanMessage(
                content="search for 3 job postings for an ai engineer using langchain in bengaluru on linkedin and list their details"
            )
        }
    )
    print(result)


if __name__ == "__main__":
    main()
