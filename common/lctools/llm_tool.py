from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


llm = ChatOpenAI(model='gpt-3.5-turbo-0613', streaming=True, callbacks=[StreamingStdOutCallbackHandler()])


def run_review(content):
    try:
        return llm.call_as_llm(f"Please review the content in Chinese: {content}")
    except Exception as err:
        print(err)
        return "Failed"


def run_summary(content):
    try:
        return llm.call_as_llm(f"Please summary the content in Chinese: {content}")
    except Exception as err:
        print(err)
        return "Failed"
