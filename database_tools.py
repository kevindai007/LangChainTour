import getpass
import os

from langchain import hub
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

    print(db.get_usable_table_names())
    db.run("SELECT * FROM users")

    # Create chain for SQL generation
    test_chain = create_sql_query_chain(model, db)
    # resp = test_chain.invoke(
    #     {"question": "please tell me how many users are there in the database?you should only output the result"})
    # print(resp)
    toolkit = SQLDatabaseToolkit(db=db, llm=model)
    print(toolkit.get_tools())


    prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
    assert len(prompt_template.messages) == 1
    print(prompt_template.input_variables)
    print(prompt_template)

    system_message = prompt_template.format(dialect="Postgresql", top_k=5)
    agent_executor = create_react_agent(model, toolkit.get_tools(), prompt=system_message)

    example_query = "please tell me the first user's role?"

    events = agent_executor.stream(
        {"messages": [("user", example_query)]},
        stream_mode="values",
    )
    for event in events:
        event["messages"][-1].pretty_print()




