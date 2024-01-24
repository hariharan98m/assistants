from llama_index import ServiceContext, LLMPredictor, OpenAIEmbedding, PromptHelper
from llama_index.llms import OpenAI
from llama_index.text_splitter import TokenTextSplitter
from llama_index.node_parser import SimpleNodeParser
from llama_index import SimpleDirectoryReader, VectorStoreIndex
import tiktoken
import time
import gradio as gr
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

import gradio as gr
import numpy as np
import time

class Shadow():
    def __init__(self, directory, model = 'gpt-3.5-turbo-1106'):
        llm = OpenAI(model=model, temperature=0, max_tokens=256)

        embed_model = OpenAIEmbedding()

        text_splitter = TokenTextSplitter(
            separator=" ",
            chunk_size=1024,
            chunk_overlap=20,
            backup_separators=["\n"],
            tokenizer=tiktoken.encoding_for_model("gpt-3.5-turbo").encode
        )

        prompt_helper = PromptHelper(
            context_window=4096,
            num_output=256,
            chunk_overlap_ratio=0.1,
            chunk_size_limit=None
        )

        service_context = ServiceContext.from_defaults(
            llm=llm,
            text_splitter = text_splitter,
            embed_model=embed_model,
            prompt_helper=prompt_helper
        )

        documents = SimpleDirectoryReader(input_dir=directory).load_data()
        index = VectorStoreIndex.from_documents(
            documents,
            service_context = service_context
        )
        index.storage_context.persist()

        self.query_engine = index.as_chat_engine(streaming=True)

    def asst_chat(self, human_message, history):
        streaming_response = self.query_engine.stream_chat(human_message)
        cont_text = ""
        for text in streaming_response.response_gen:
            # do something with text as they arrive.
            print(text)
            cont_text+=text
            time.sleep(0.05)
            yield cont_text

shadow = Shadow(directory = 'data', model = 'gpt-4-1106-preview') # pass path discoverable files to the shadow agent.

demo = gr.ChatInterface(shadow.asst_chat, title="Shadow - LLamaindex RAG")
demo.queue()
demo.launch()