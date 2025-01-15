from vertexai.preview import rag
from vertexai.preview.generative_models import GenerativeModel, Tool
import vertexai

from credentials import *

# Create a RAG Corpus, Import Files, and Generate a response


class Model:
    # Initialize Vertex AI API once per session
    def __init__(self):
        self.__chat = None
        self.__rag_corpus = None
        self.__rag_model = None
        vertexai.init(project=project_id, location=location)

        # Configure embedding model, for example "text-embedding-004", using RagCorpus
        self.__embedding_model_config = rag.EmbeddingModelConfig(
            publisher_model="publishers/google/models/text-embedding-004"
        )

    def init_rag_corpus(self, corpus_name):
        self.__rag_corpus = rag.create_corpus(
            display_name=corpus_name,
            embedding_model_config=self.__embedding_model_config,
        )

        # Import Files to the RagCorpus
        rag.import_files(
            self.__rag_corpus.name,
            paths,
            chunk_size=512,  # Optional
            chunk_overlap=100,  # Optional
            max_embedding_requests_per_min=900,  # Optional
        )

    def init_llm(self, has_rag_corpus=True):
        # Create a RAG retrieval tool
        if has_rag_corpus:
            rag_retrieval_tool = Tool.from_retrieval(
                retrieval=rag.Retrieval(
                    source=rag.VertexRagStore(
                        rag_resources=[
                            rag.RagResource(
                                rag_corpus=self.__rag_corpus.name,  # Currently only 1 corpus is allowed.
                                # Optional: supply IDs from `rag.list_files()`.
                                # rag_file_ids=["rag-file-1", "rag-file-2", ...],
                            )
                        ],
                        similarity_top_k=3,  # Optional
                        vector_distance_threshold=0.5,  # Optional
                    ),
                )
            )
            # Create a model instance with rag tool
            self.__rag_model = GenerativeModel(
                model_name=model_name, tools=[rag_retrieval_tool]
            )
        else:
            self.__rag_model = GenerativeModel(
                model_name=model_name
            )
        # Initialize chat in model
        self.__chat = self.__rag_model.start_chat()

    # chat to test in command client
    def chat_cmd(self):
        # Generate response
        chat = self.__chat
        question = input("Enter a question or type 'quit' to quit: ")
        while question != "\n" and question != 'quit':
            response = chat.send_message(question)
            print('Below is response from chat query: ')
            print(response.text)
            question = input("Enter a question or type 'quit' to quit: ")

    # chat for api call
    def chat(self, message: str):
        chat = self.__chat
        response = chat.send_message(message).text
        print('Below is response from chat query: ')
        print(response.text)
        return response.text


if __name__ == '__main__':
    model = Model()
    model.init_rag_corpus("sample-article1-corpus")
    model.init_llm()
    model.chat_cmd()

