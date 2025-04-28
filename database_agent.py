import getpass
import os

from langchain import hub
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain.chat_models import init_chat_model
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

if __name__ == '__main__':
    if not os.environ.get("ANTHROPIC_API_KEY"):
        os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter API key for Anthropic: ")

    model = init_chat_model("claude-3-5-sonnet-latest")

    HOST = "localhost"
    PORT = 5432
    DATABASE = "authserver"
    USERNAME = "postgres"
    PASSWORD = "postgres"
    POSTGRESQL_DB_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(USERNAME, PASSWORD, HOST, PORT, DATABASE)
    db = SQLDatabase.from_uri(POSTGRESQL_DB_URI)


    toolkit = SQLDatabaseToolkit(db=db, llm=model)
    tools = toolkit.get_tools()

    #use agent to integrate database and model
    prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
    # print(prompt_template.messages)

    system_message = prompt_template.format(dialect="Postgresql", top_k=5)
    agent_executor = create_react_agent(model, tools, prompt=SystemMessage(system_message))
    example_query = "please tell me the first user's role?"
    resp = agent_executor.invoke({"messages": [("user", example_query)]})
    print(resp["messages"])
    result = resp["messages"][-1].content
    print(result)



