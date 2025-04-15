import getpass
import json
import os

import bs4
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chat_models import init_chat_model
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

if __name__ == '__main__':
    if not os.environ.get("ANTHROPIC_API_KEY"):
        os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter API key for Anthropic: ")
    model = init_chat_model("claude-3-5-sonnet-latest")

    loader = WebBaseLoader(
        web_paths=['https://lilianweng.github.io/posts/2023-06-23-agent/'],
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(class_=("post-header", "post-title", "post-content")),
        ),
    )

    docs = loader.load()
    # print(docs)
    docs_dict = [doc.dict() for doc in docs]
    print(json.dumps(docs_dict, indent=4, ensure_ascii=False))

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_documents = splitter.split_documents(docs)
    # for split_document in split_documents:
    #     print(split_document)

    vector_store = Chroma.from_documents(documents=split_documents, embedding=OpenAIEmbeddings())
    retriever = vector_store.as_retriever()

    system_message = """
    u are an assistant for question answering tasks. Use the following pieces of retrieved context to answer the question at the end. If you don't know the answer, just say "I don't know". Don't try to make up an answer.
    
    {context}
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("human", "{input}")
        ]
    )

    chain = create_stuff_documents_chain(model, prompt)

    chain2 = create_retrieval_chain(retriever,chain)
    resp = chain2.invoke({"input": "what is the difference between react agent and react doc agent?"})
    print(resp)
    resp = chain2.invoke({"input": "what's task decomposition?"})
    print(resp)
