import getpass
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate



if __name__ == '__main__':
    import getpass
    import os

    if not os.environ.get("ANTHROPIC_API_KEY"):
        os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter API key for Anthropic: ")

    model = init_chat_model("claude-3-5-sonnet-latest")

    # messages = [
    #     SystemMessage("Translate the following from English into Chinese,you should only output the result"),
    #     HumanMessage("Can you can a can as a canner can can a can?"),
    # ]
    # response = model.invoke(messages)
    # print(response)

    # stream output
    # for token in model.stream(messages):
    #     print(token.content, end=" | ")

    system_template = "Translate the following from English into {language},you should only output the result"
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{text}")]
    )
    prompt = prompt_template.invoke({"language": "English", "text": "不吃老人言,吃亏在眼前"})
    print(prompt.to_messages())
    response = model.invoke(prompt)
    print(response.content)

