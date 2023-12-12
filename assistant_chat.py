from openai import OpenAI
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()


def run_open_ai():
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        organization=os.getenv("OPENAI_ORGANISATION_ID"),
    )

    assistant = client.beta.assistants.retrieve(assistant_id=os.getenv("ASSISTANT_ID"))

    # create a thread
    thread = client.beta.threads.create()
    thread.id = thread.id

    # add message to thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Please can you draft an email with a detailed summary in bullet point format of what has been happening in sudan. At the top i would like you to use numbers to summarise RSF vs Army statistics. Please assume I will be sending this directly so only give me the content without the subject. I would like it to be a 5+ minute read with quotes from the links, along with source (name of website). Please also warn readers that this is AI generated and that this is an experiment. Please sign it off with a mysterious alias.",
    )

    # run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="You are a political analyst covering sudan. You are tasked with providing an update each morning to update knowledgable people on the latest on clashes in Sudan. Sudan News Sweep is the roundup. The other files are pdf versions of the links in Sudan News Sweep.",
    )

    # display the response
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # retrieve and add to thread
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    text = messages.dict()["data"][0]["content"][0]["text"]["value"]
    return text
