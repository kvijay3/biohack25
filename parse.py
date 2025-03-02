#LLAMA_CLOUD_API_KEY
# bring in our LLAMA_CLOUD_API_KEY
import os
from dotenv import load_dotenv
load_dotenv()

# bring in deps
from llama_cloud_services import LlamaParse
from llama_index.core import SimpleDirectoryReader

def parse_upload(file_location):
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
        input_files=[file_location], 
        file_extractor=file_extractor
        ).load_data()

    return documents