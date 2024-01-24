from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
import time
import gradio as gr
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  # Replace with your key

from openai import OpenAI
client = OpenAI()

# using langchain
llm = ChatOpenAI(temperature=1.0, model='gpt-4')

def predict(message, history):
    history_langchain_format = []
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=message))
    gpt_response = llm(history_langchain_format)
    return gpt_response.content


class Shadow():
    def __init__(self, files, model = 'gpt-3.5-turbo-1106'):
        # knowledge base of the agent.
        file_ids = []
        for file in files:
            file = client.files.create(
                file=open("wiki.txt", "rb"),
                purpose='assistants'
            )
            file_ids.append(file.id)

        # assistant created out of the knowledge.
        self.assistant = client.beta.assistants.create(
            instructions='''You are a code helper. Your role is now focused solely on helping users with terminal commands.
            Provide guidance on using various shell commands, explain command line interfaces, and assist in troubleshooting terminal issues.
            Offer clear, step-by-step instructions for executing and understanding terminal commands. Avoid providing commands that could be harmful or irreversible without proper warning.
            If unclear about the user's requirements, ask for clarification.
            Your responses should be informative, precise, and tailored to users ranging from beginners to advanced.''',
            # model="gpt-4-1106-preview",
            model =model,
            tools=[{"type": "retrieval"}],
            file_ids=file_ids
        )
        # chat thread with the agent.
        self.thread = client.beta.threads.create()

    def asst_chat(self, human_message, history):
        # add this message to the chat thread.
        message = client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=human_message
        )
        # create a run to execute this message against the shadow assistant.
        run = client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )
        # keep checking the status of the run until it is completed.
        s = time.time()
        while client.beta.threads.runs.retrieve(
            thread_id=self.thread.id,
            run_id=run.id
        ).status != 'completed':
            pass
        e = time.time()
        print(f"Time taken for the run to complete: {e-s} seconds")

        # get the response from the shadow assistant.
        messages = client.beta.threads.messages.list(
            thread_id=self.thread.id
        )
        ai_message = messages.data[0].content[0].text.value
        return ai_message

shadow = Shadow(files = ['data/wiki.txt']) # pass path discoverable files to the shadow agent.
gr.ChatInterface(shadow.asst_chat, title="Shadow - Assistants API").launch()