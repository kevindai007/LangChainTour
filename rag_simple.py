import getpass
import os

from langchain.chat_models import init_chat_model
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system", "You talk like a pirate. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

if __name__ == '__main__':
    if not os.environ.get("ANTHROPIC_API_KEY"):
        os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter API key for Anthropic: ")

    model = init_chat_model("claude-3-5-sonnet-latest")

    documents = [
        Document(
            page_content="Dog is popular pet, it is loyal and friendly.",
            metadata={"source": "dog pet doc"}
        ),
        Document(
            page_content="Cat is popular pet, it is independent and playful.",
            metadata={"source": "cat pet doc"}
        ),
        Document(
            page_content="Bird is popular pet, it is colorful and chirpy.",
            metadata={"source": "bird pet doc"}
        ),
        Document(
            page_content="Fish is popular pet, it is easy to maintain and quiet.",
            metadata={"source": "fish pet doc"}
        ),
        Document(
            page_content="Rabbit is popular pet, it is cute and fluffy.",
            metadata={"source": "rabbit pet doc"}
        ),
        Document(
            page_content="Hamster is popular pet, it is small and active.",
            metadata={"source": "hamster pet doc"}
        ),
    ]

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    vector_store = Chroma.from_documents(documents, embedding=embeddings)
    # the less the score is, the more similar the two sentences are
    # print(vector_store.similarity_search_with_score("Dog is loyal and friendly."))
    # print(vector_store.similarity_search_with_score("狗狗是我们忠诚的朋友"))

    retriever = RunnableLambda(vector_store.similarity_search, ).bind(k=1)
    # print(retriever.batch(["shark", "bird"]))

    message = """
        please use the provided context to answer the following questions:
        {question}
        ccontext:
        {context}
    """
    prompt_template = ChatPromptTemplate.from_messages([('human', message)])

    #RunnablePassthrough allows us to pass the user question to prompt and model later
    chain = {'question': RunnablePassthrough(), 'context': retriever} | prompt_template | model;
    resp = chain.invoke("please tell me something about cat")
    print(resp.content)