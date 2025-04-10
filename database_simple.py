import getpass
import os
from operator import itemgetter

from langchain.chat_models import init_chat_model
from langchain_community.tools import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough


def clean_query(inputs):
    raw_query = inputs["query"]
    cleaned_query = raw_query.strip()
    if "SQLQuery:" in cleaned_query:
        cleaned_query = cleaned_query.split("SQLQuery:")[-1].strip()
    return {**inputs, "query": cleaned_query}


def create_sql_query_chain(model, db):
    sql_prompt = PromptTemplate.from_template("""
        You are an expert in SQL and PostgreSQL. You are working with the following schema:
            
            - Table `users(id, username, password, email, created_time, updated_time)`
            - Table `roles(id, name, description, created_time, updated_time)`
            - Table `user_roles(id, user_id, role_id, created_time, updated_time)`
            
            Each user can have multiple roles. To get user roles, use JOIN between `users`, `user_roles`, and `roles`.
            
            Now, write a valid SQL query for the following question:
            Question: {question}
            Only return the SQL query. Do not include explanation or prefixes.
        """)

    return sql_prompt | model | StrOutputParser()


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

    answer_template = PromptTemplate.from_template(
        """
        please answer the following question based on the provided SQL query and result:
        QUESTION: {question}
        SQL_QUERY: {query}
        SQL_RESULT: {result}
        Answer:
        """,
    )

    execute_sql_tool = QuerySQLDataBaseTool(db=db)
    chain = (RunnablePassthrough.assign(query=test_chain).assign(result=itemgetter("query") | execute_sql_tool)
             | answer_template
             | model
             | StrOutputParser()
             )

    # resp = chain.invoke(
    #     {"question": "please tell me how many users are there in the database?you should only output the result"})
    # print(resp)

    # resp = chain.invoke(
    #     {"question": "please tell me the user role of the first user"})
    # print(resp)
