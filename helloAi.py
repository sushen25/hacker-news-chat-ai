import os
from haystack import Pipeline, Document, component 
from haystack.utils import Secret
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders.prompt_builder import PromptBuilder

# Write documents to InMemoryDocumentStore
# document_store = InMemoryDocumentStore()
# document_store.write_documents([
#     Document(content="My name is Jean and I live in Paris."), 
#     Document(content="My name is Mark and I live in Berlin."), 
#     Document(content="My name is Giorgio and I live in Rome.")
# ])

@component
class DialogStarter:
    @component.output_types(starter_dialog=str)
    def run(self, name: str):
        return { "starter_dialog": f"{name} is in the middle of an abandoned city."}

# Build a RAG pipeline
prompt_template = """ You will be given the beginning of a dialogue. 
Create a short play script using this as the start of the play.
Start of dialogue: {{ dialogue }}
Full script: 
"""

# retriever = InMemoryBM25Retriever(document_store=document_store)
dialog_starter = DialogStarter()
prompt_builder = PromptBuilder(template=prompt_template)
llm = OpenAIGenerator()

rag_pipeline = Pipeline()
rag_pipeline.add_component("dialog_starter", dialog_starter)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", llm)

rag_pipeline.connect("dialog_starter.starter_dialog", "prompt_builder.dialogue")
rag_pipeline.connect("prompt_builder", "llm")

rag_pipeline.draw("./pipeline.png")

# Ask a question
name = "Andy Noh"
results = rag_pipeline.run(
    {
        "dialog_starter": {"name": name}
    }
)

print(results["llm"]["replies"])