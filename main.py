import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
load_dotenv()


@tool
def sundaranbu(name:str)->str:
    """
    This tool will use rag/sundaranbu.md file to answer the question. if question is not related to sundaranbu.md file, return "I don't know"
    """
    with open("rag/sundaranbu.md", "r") as file:
        content = file.read()
    return content


@tool
def hasan(name:str)->str:
    """
    This tool will use rag/hasan.md file to answer the question. if question is not related to hasan.md file, return "I don't know"
    """
    with open("rag/hasan.md", "r") as file:
        content = file.read()
    return content

def data():
    llm = ChatOpenAI(model="gpt-4o-mini",temperature=1)
    tools = [sundaranbu, hasan]
    agent = create_agent(llm,tools)
    result = agent.invoke({"messages":[("user","what is hasan full name ?")]})
    print(result)

data()

