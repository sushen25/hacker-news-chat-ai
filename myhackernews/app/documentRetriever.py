import requests

from haystack import Pipeline, Document, component
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument

@component
class DocumentRetriever:
    def __init__(self):
        pipeline = Pipeline()

        fetcher = LinkContentFetcher()
        converter = HTMLToDocument()

        pipeline.add_component("fetcher", fetcher)
        pipeline.add_component("converter", converter)

        pipeline.connect("fetcher.streams", "converter.sources")
        self.pipeline = pipeline

    def fetch_post(self, post_id: int):
        url = f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json?print=pretty"
        response = requests.get(url)
        article = response.json()
        return article

    @component.output_types(doc=Document)
    def run(self, article_id: str):
        post = self.fetch_post(article_id)

        print("POST")
        print(post)

        # TODO - implement no url handling
        if "url" not in post:
            raise ValueError(f"Post {article_id} does not have a URL")

        try:
            result = self.pipeline.run({"fetcher": {"urls": [post["url"]]}})
            print(f"Article {post['url']} fetched successfully")
            print(result["converter"]["documents"][0])
            print(result["converter"]["documents"][0].content)
        except:
            print(f"Error fetching Article {post["url"]}")

        return {"doc": Document(content=result["converter"]["documents"][0])}
    
