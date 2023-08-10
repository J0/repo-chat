import os
from dotenv import load_dotenv
from supabase.client import Client, create_client
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
import vecs
from vecs.adapter import Adapter, ParagraphChunker, TextEmbedding

load_dotenv()

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
DB_CONNECTION = os.environ.get("DB_CONNECTION")
TABLE_NAME = os.environ.get("TABLE_NAME")

# configure these to fit your needs
exclude_dir = ['.git', 'node_modules', 'public', 'assets']
exclude_files = ['package-lock.json', '.DS_Store']
exclude_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.ico', '.svg', '.webp',
    '.mp3', '.wav']

documents = []

for dirpath, dirnames, filenames in os.walk('repo'):
    # skip directories in exclude_dir
    dirnames[:] = [d for d in dirnames if d not in exclude_dir]
    
    for file in filenames:
        _, file_extension = os.path.splitext(file)

        # skip files in exclude_files
        if file not in exclude_files and file_extension not in exclude_extensions:
            file_path = os.path.join(dirpath, file)
            loader = TextLoader(file_path, encoding='ISO-8859-1')
            documents.extend(loader.load())


text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)
# create vector store client
print(DB_CONNECTION)
vx = vecs.create_client(DB_CONNECTION)
repo_collection = vx.get_or_create_collection(
    name=TABLE_NAME,
    # here comes the new part
    adapter=Adapter(
        [
            ParagraphChunker(skip_during_query=True),
            TextEmbedding(model='Supabase/gte-small'),
        ]
    )
)
for doc in docs:
    source = doc.metadata['source']
    cleaned_source = '/'.join(source.split('/')[1:])
    doc.page_content = "FILE NAME: " + cleaned_source + "\n###\n" + doc.page_content.replace('\u0000', '')
    repo_collection.upsert(records=[(
     f"{hash(doc.page_content)}",
     doc.page_content,
     doc.metadata)])
