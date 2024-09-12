import requests

from haystack import Pipeline, Document, component
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument
from app.crud import does_post_exist

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

        ids = []
        i = 0
        while i < len(article_ids) and len(ids) < num_posts:
            if not does_post_exist(article_ids[i]):
                ids.append(article_ids[i])
            i += 1 

        return ids
    
    def fetch_post(self, post_id: int):
        url = f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json?print=pretty"
        response = requests.get(url)
        article = response.json()
        return article

    @component.output_types(articles=List[Document], ids = List[int])
    def run(self, num_articles: int):
        articles = []
        ids = []
        top_post_ids = self.get_top_post_ids(num_articles)

        for id in top_post_ids:
            post = self.fetch_post(id)
            if "url" in post:
                try:
                    article = self.fetching_pipeline.run({"fetcher": {"urls": [post["url"]]}})
                    articles.append(article["converter"]["documents"][0])
                    ids.append(id)
                except:
                    print(f"Error fetching article {post['url']}")
            elif "text" in post:
                try:
                    articles.append(Document(content=post["text"]))
                    ids.append(id)
                except:
                    print(f"Error fetching article {post['text']}")
        
        return { "articles": articles, "ids": ids }
