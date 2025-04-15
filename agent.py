import getpass
import os

from langchain.chat_models import init_chat_model
from langchain_community.tools import TavilySearchResults
from langgraph.prebuilt import chat_agent_executor

if __name__ == '__main__':
    if not os.environ.get("ANTHROPIC_API_KEY"):
        os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter API key for Anthropic: ")
    model = init_chat_model("claude-3-5-sonnet-latest")

    search = TavilySearchResults(max_results=2)
    # print(search.invoke({"query": "how is the weather in Abu Dhabi today?"}))

    # model will determine the best tool to use, and will choose to use the tool or not
    # model_bind_tools = model.bind_tools([search])
    # resp = model_bind_tools.invoke([SystemMessage("you should always give the shortest answer to the user"),HumanMessage("how is the weather in Abu Dhabi today?")])
    # print(resp.content)
    # print('--------')
    # print(resp.tool_calls)

    tools = [search]
    model_bind_tools = model.bind_tools(tools)

    agent_executor = chat_agent_executor.create_tool_calling_executor(model_bind_tools, tools)
    resp = agent_executor.invoke({"messages": [("system",
                                                "you should always give the shortest answer to the user,eg:question:'how is the weather in Abu Dhabi today?',answer:'Abu Dhabi:35.2°C'"),
                                               ("user", "how is the weather in Abu Dhabi today?")]})
    print(resp["messages"])
