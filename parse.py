#LLAMA_CLOUD_API_KEY
# bring in our LLAMA_CLOUD_API_KEY
import os
from dotenv import load_dotenv
load_dotenv()

# bring in deps
from llama_cloud_services import LlamaParse
from llama_index.core import SimpleDirectoryReader


LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
if not LLAMA_CLOUD_API_KEY:
    raise ValueError("API Key is missing. Please check your .env file.")

# set up parser
parser = LlamaParse(
    result_type="markdown"  # "markdown" and "text" are available
)

# use SimpleDirectoryReader to parse our file
file_extractor = {".pdf": parser}
documents = SimpleDirectoryReader(
    input_files=[r'/mnt/c/Users/Vijay/Desktop/biohack25/sample-pdfs/sample_ehr.pdf'], 
    file_extractor=file_extractor
    ).load_data()

print(documents)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("API Key is missing. Please check your .env file.")

from llama_index.core import VectorStoreIndex

# create an index from the parsed markdown
index = VectorStoreIndex.from_documents(documents)

# create a query engine for the index
query_engine = index.as_query_engine()

# query the engine
query = "What is my Metformin Level?"
response = query_engine.query(query)
print(response)