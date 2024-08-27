from hackerNewsFetcher import HackerNewsFetcher
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from haystack import Pipeline


def get_top_news():
    fetcher = HackerNewsFetcher()

    prompt_template = """  
    You will be provided a few of the top posts in HackerNews, followed by their URL.  
    For each post, provide a brief summary followed by the URL the full post can be found at.  
    
    Posts:  
    {% for article in articles %}  
    {{ article.content }}
    URL: {{ article.meta["url"] }}
    {% endfor %}  
    """

    prompt_builder = PromptBuilder(template=prompt_template)
    llm = OpenAIGenerator()

    pipeline = Pipeline()

    pipeline.add_component("fetcher", fetcher)
    pipeline.add_component("prompt_builder", prompt_builder)
    pipeline.add_component("llm", llm)

    pipeline.connect("fetcher.articles", "prompt_builder.articles")
    pipeline.connect("prompt_builder", "llm")

    pipeline.draw("./pipeline.png")

    result = pipeline.run({"fetcher": {"num_articles": 5}})

    print("RESULT")
    print(result)

    return result["llm"]["replies"]

# Hacker News Fetcher
    # Fetcher
    # Converter
# Prompt Builder 
# LLM


