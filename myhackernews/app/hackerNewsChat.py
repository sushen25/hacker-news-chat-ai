import pprint
from typing import List
from haystack import component, Pipeline, Document
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from haystack.components.generators.chat.openai import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage
from haystack.components.joiners import BranchJoiner
from haystack.components.converters import OutputAdapter
from haystack_experimental.components.tools import OpenAIFunctionCaller

from documentRetriever import DocumentRetriever

@component
class PropmtToChatMessage:
    @component.output_types(chat_message=List[ChatMessage])
    def run(self, prompt: str):
        print("Prompt to Chat Message ----------------")
        print(prompt)
        return {"chat_message": [ChatMessage.from_system(prompt)]}

def hackerNewsChat():
    pipeline = Pipeline()

    fetcher = DocumentRetriever()
    prompt_template =  """
    You are a chatbot designed to answer questions about the Hacker News Article that's provided to you.
    Don't make things up or provide false information. If you don't know the answer, just say so.
    Only answer questions about the article that's provided to you. Don't go off-topic.

    Article:
    {{ article.content.content }}
    """
    prompt_builder = PromptBuilder(prompt_template)
    prompt_to_chat_message = PropmtToChatMessage()
    
    pipeline.add_component("fetcher", fetcher)
    pipeline.add_component("prompt_builder", prompt_builder)
    pipeline.add_component("prompt_to_chat_message", prompt_to_chat_message)

    pipeline.connect("fetcher.doc", "prompt_builder.article")
    pipeline.connect("prompt_builder", "prompt_to_chat_message")

    pipeline.draw("./hackerNewsChat.png")

    results = pipeline.run({"fetcher": {"article_id": "42178761"}})

    return results["prompt_to_chat_message"]["chat_message"]

def chatAgent(messages: List[ChatMessage]):
    chat_generator = OpenAIChatGenerator(model="gpt-3.5-turbo")
    response = chat_generator.run(messages)

    return response["replies"]

def main():
    messages = hackerNewsChat()
    while True:
        user_input = input("INFO: Type 'exit' or 'quit' to stop\n")
        if user_input.lower() == "exit" or user_input.lower() == "quit":
            break
        messages.append(ChatMessage.from_user(user_input))
        response = chatAgent(messages)
        print("AGENT: ")
        pprint.pprint(response[0].content)

        messages.extend(response)


if __name__ == "__main__":
    main()