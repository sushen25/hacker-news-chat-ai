import json

from hackerNewsFetcher import HackerNewsFetcher
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from haystack import Pipeline, component
from typing import List, Optional
from colorama import Fore
from pydantic import BaseModel, ValidationError


class Post(BaseModel):
    title: str
    summary: str
    url: str


class Posts(BaseModel):
    posts: List[Post]

@component
class OutputValidator:
    def __init__(self, pydantic_model: BaseModel):
        self.pydantic_model = pydantic_model
        self.iteration_counter = 0

    # Define the component output
    @component.output_types(valid_replies=List[str], invalid_replies=Optional[List[str]], error_message=Optional[str])
    def run(self, replies: List[str]):

        self.iteration_counter += 1

        ## Try to parse the LLM's reply ##
        # If the LLM's reply is a valid object, return `"valid_replies"`
        try:
            output_dict = json.loads(replies[0])
            self.pydantic_model.parse_obj(output_dict)
            print(
                Fore.GREEN
                + f"OutputValidator at Iteration {self.iteration_counter}: Valid JSON from LLM - No need for looping: {replies[0]}"
            )
            return {"valid_replies": replies}

        # If the LLM's reply is corrupted or not valid, return "invalid_replies" and the "error_message" for LLM to try again
        except (ValueError, ValidationError) as e:
            print(
                Fore.RED
                + f"OutputValidator at Iteration {self.iteration_counter}: Invalid JSON from LLM - Let's try again.\n"
                f"Output from LLM:\n {replies[0]} \n"
                f"Error from OutputValidator: {e}"
            )
            return {"invalid_replies": replies, "error_message": str(e)}


def get_top_news():
    fetcher = HackerNewsFetcher()

    prompt_template = """  
    You will be provided a few of the top posts in HackerNews, followed by their URL.  
    For each post, summarise the posts highlighting the main points and output a JSON object folling the schema.
    {{ schema }}
    Make sure the output is a valid JSON string.  

    Posts:  
    {% for article in articles %}  
    {{ article.content }}
    URL: {{ article.meta["url"] }}
    {% endfor %}

    {% if invalid_replies and error_message %}
        You already created the following output in a previous attempt: {{invalid_replies}}
        However, this doesn't comply with the format requirements from above and triggered this Python exception: {{error_message}}
        Correct the output and try again. Just return the corrected output without any extra explanations.
    {% endif %}
    """

    prompt_builder = PromptBuilder(template=prompt_template)
    llm = OpenAIGenerator()
    output_validator = OutputValidator(pydantic_model=Posts)

    pipeline = Pipeline()

    pipeline.add_component("fetcher", fetcher)
    pipeline.add_component("prompt_builder", prompt_builder)
    pipeline.add_component("llm", llm)
    pipeline.add_component("output_validator", output_validator)

    pipeline.connect("fetcher.articles", "prompt_builder.articles")
    pipeline.connect("prompt_builder", "llm")
    pipeline.connect("llm", "output_validator")

    pipeline.connect("output_validator.invalid_replies", "prompt_builder.invalid_replies")
    pipeline.connect("output_validator.error_message", "prompt_builder.error_message")


    # pipeline.draw("./pipeline.png")

    result = pipeline.run({"fetcher": {"num_articles": 5}, "prompt_builder": {"schema": Posts.schema_json()}})

    return json.loads(result["output_validator"]["valid_replies"][0])

if __name__ == "__main__":
    get_top_news()
    # print(Posts.schema_json())
    # print(json.dumps(top_news, indent=2))


