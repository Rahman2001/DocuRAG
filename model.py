import os

from llama_index.core import Settings
from llama_index.llms.vertex import Vertex
from llama_index.indices.managed.vertexai import VertexAIIndex
from credentials import *

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

global query_engine
query_engine = None



def init_llm():
    vertex_gemini = Vertex(
        model="gemini-1.5-pro-preview-0514",
        temperature=0,
        context_window=100000,
        additional_kwargs={}
    )
    Settings.llm = vertex_gemini


def init_index():

    # Optional: If creating a new corpus
    corpus_display_name = "docusign-corpus"
    corpus_description = "Vertex AI Corpus for LlamaIndex"

    # Create a corpus or provide an existing corpus ID
    index = VertexAIIndex(
        project_id=project_id,
        location=location,
        corpus_display_name=corpus_display_name,
        corpus_description=corpus_description,
        show_progress=True
    )
    print(f"Newly created corpus name is {index.corpus_name}.")

    # Upload local file
    file_name = index.insert_file(
        file_path="docs/paul_graham_essay.txt",
        metadata={
            "display_name": "paul_graham_essay",
            "description": "Paul Graham essay",
        },
    )
    print(index.list_files())
    return index


def init_query_engine(index):
    global query_engine
    query_engine = index.as_query_engine(similarity_top_k=3)

    return query_engine


def chat(input_question):
    global query_engine

    # Querying.
    response = query_engine.query("What did Paul Graham do growing up?")

    # Show response.
    # print(f"Response is {response.response}")

    # # Show cited passages that were used to construct the response.
    # for cited_text in [node.text for node in response.source_nodes]:
    #     print(f"Cited text: {cited_text}")

    # Show answerability. 0 means not answerable from the passages.
    # 1 means the model is certain the answer can be provided from the passages.
    # if response.metadata:
    #     print(
    #         f"Answerability: {response.metadata.get('answerable_probability', 0)}"
    #     )
    return response.response


def chat_cmd():
    global query_engine

    while True:
        input_question = input("Enter your question (or 'exit' to quit): ")
        if input_question.lower() == 'exit':
            break

        response = query_engine.query(input_question)
        logging.info("got response from llm - %s", response)


if __name__ == '__main__':
    init_llm()
    index = init_index()
    init_query_engine(index)
    chat_cmd()
