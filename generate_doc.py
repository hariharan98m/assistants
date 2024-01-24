import os
from dotenv import load_dotenv
load_dotenv()
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

from openai import OpenAI
client = OpenAI()

def generate_wiki(logfile = 'ec2.log', outputfile = 'wiki.txt'):

    file = client.files.create(
        file=open(logfile, "rb"),
        purpose='assistants'
    )
    thread = client.beta.threads.create()

    instructions = """This is log of a developer's terminal session.
    Identify their high-level goals and the sequence of low-level commands they ran to achieve them.
    Write a wiki page with these topics giving their step-wise instructions.
    This wiki will serve as documentation for other team mates to refer and use in their work.
    So you should discard any basic commands tried during course of their exploration, and probably document plausible errors and how to debug them."""

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=instructions,
        file_ids=[file.id]
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id
    )

    while client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    ).status != 'completed':
        pass

    # get the response from the shadow assistant.
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    ai_message = messages.data[0].content[0].text.value

    # write to the wiki.
    with open(outputfile, 'a') as f:
        f.write(ai_message + '\n')
        f.write('----------------------------------------\n')

if __name__ == "__main__":
    generate_wiki()