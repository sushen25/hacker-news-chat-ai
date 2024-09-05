import requests

from haystack import Pipeline, Document, component
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument

from typing import List

@component
class HackerNewsFetcher:
    def __init__(self):
        fetching_pipeline = Pipeline()

        fetcher = LinkContentFetcher()
        converter = HTMLToDocument()

        fetching_pipeline.add_component("fetcher", fetcher)
        fetching_pipeline.add_component("converter", converter)

        fetching_pipeline.connect("fetcher.streams", "converter.sources")
        self.fetching_pipeline = fetching_pipeline

    def get_top_post_ids(self, num_posts: int = 7):
        url = f"https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
        response = requests.get(url)
        article_ids = response.json()
        return article_ids[:num_posts]
    
    def fetch_post(self, post_id: int):
        url = f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json?print=pretty"
        response = requests.get(url)
        article = response.json()
        return article

    @component.output_types(articles=List[Document])
    def run(self, num_articles: int):
        articles = []
        top_post_ids = self.get_top_post_ids(num_articles)

        for id in top_post_ids:
            post = self.fetch_post(id)
            if "url" in post:
                try:
                    article = self.fetching_pipeline.run({"fetcher": {"urls": [post["url"]]}})
                    articles.append(article["converter"]["documents"][0])
                except:
                    print(f"Error fetching article {post['url']}")
            elif "text" in post:
                try:
                    articles.append(Document(content=post["text"]))
                except:
                    print(f"Error fetching article {post['text']}")
        
        return { "articles": articles}
