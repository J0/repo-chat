import os
import vecs
from dotenv import load_dotenv
from langchain import LLMChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import (
    SystemMessage
)
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from vecs.adapter import Adapter, ParagraphChunker, TextEmbedding

load_dotenv()

DB_CONNECTION = os.environ.get("DB_CONNECTION")
TABLE_NAME = os.environ.get("TABLE_NAME")
vx = vecs.create_client(DB_CONNECTION)
docs = vx.get_or_create_collection(
    name=TABLE_NAME,
    # here comes the new part
    adapter=Adapter(
        [
            ParagraphChunker(skip_during_query=True),
            TextEmbedding(model='Supabase/gte-small'),
        ]
    )
)
docs.create_index()

while True:
    query = input("\033[34mWhat question do you have about your repo?\n\033[0m")

    if query.lower().strip() == "exit":
        print("\033[31mGoodbye!\n\033[0m")
        break
    # Change the number of documents fetched according to your needs. Defaults to 7
    matched_docs = docs.query(data=query, include_metadata=True, limit=7)
    code_str = ""

    for id, metadata in matched_docs:
        code_str += metadata["body"]+ "\n\n"
        
    print("\n\033[35m" + code_str + "\n\033[32m")

    
    template="""
    You are Codebase AI. You are a superintelligent AI that answers questions about codebases.

    You are:
    - helpful & friendly
    - good at answering complex questions in simple language
    - an expert in all programming languages
    - able to infer the intent of the user's question

    The user will ask a question about their codebase, and you will answer it.

    When the user asks their question, you will answer it by searching the codebase for the answer.

    Here is the user's question and code file(s) you found to answer the question:

    Question:
    {query}

    Code file(s):
    {code}
    
    [END OF CODE FILE(S)]w

    Now answer the question using the code file(s) above.
    """

    chat = ChatOpenAI(streaming=True, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), verbose=True, temperature = 0.5)
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])
    chain = LLMChain(llm=chat, prompt=chat_prompt)

    chain.run(code=code_str, query=query)

    print("\n\n")
