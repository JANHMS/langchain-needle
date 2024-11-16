# Needle

[Needle](https://needle-ai.com) makes it easy to create your Retrieval-Augmented Generation (RAG) pipelines with minimal effort.

For more details, refer to our [API documentation](https://docs.needle-ai.com/docs/api-reference/needle-api).

---

## Overview

The Needle Document Loader is a utility for integrating Needle collections with LangChain. It enables seamless storage, retrieval, and utilization of documents for RAG workflows.

This guide demonstrates:

- Storing documents into a Needle collection.
- Setting up a retriever to fetch documents.
- Building a RAG pipeline.

---

## Setup

Before starting, ensure the following environment variables are set:

- `NEEDLE_API_KEY`: Your API key for authenticating with Needle.
- `OPENAI_API_KEY`: Your OpenAI API key for language model operations.

---

## Initialization

To initialize the `NeedleLoader`, use the following parameters:

- `needle_api_key`: Your Needle API key (or set it as an environment variable).
- `collection_id`: The ID of the Needle collection to work with.

```python
import os

os.environ["NEEDLE_API_KEY"] = "your_needle_api_key"
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
```
## Load Documents
To add files to the Needle collection:

```python
from langchain_community.document_loaders.needle import NeedleLoader

collection_id = "clt_01J87M9T6B71DHZTHNXYZQRG5H"

# Initialize NeedleLoader to store documents to the collection
document_loader = NeedleLoader(
    needle_api_key=os.getenv("NEEDLE_API_KEY"),
    collection_id=collection_id,
)

files = {
    "tech-radar-30.pdf": "https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2024/04/tr_technology_radar_vol_30_en.pdf"
}

document_loader.add_files(files=files)

# Optionally, load all documents in the collection
# collections_documents = document_loader.load()
```

## Full Example: RAG Pipeline
Below is a complete example of setting up a RAG pipeline with Needle:

```python
import os

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.retrievers.needle import NeedleRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(temperature=0)

# Initialize the Needle retriever
retriever = NeedleRetriever(
    needle_api_key=os.getenv("NEEDLE_API_KEY"),
    collection_id="clt_01J87M9T6B71DHZTHNXYZQRG5H",
)

# Define system prompt for the assistant
system_prompt = """
    You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question.
    If you don't know, say so concisely.\n\n{context}
"""

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("human", "{input}")]
)

# Create the question-answering chain
question_answer_chain = create_stuff_documents_chain(llm, prompt)

# Create the RAG pipeline
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Define the input query
query = {"input": "Did RAG move to accepted?"}

# Get the response
response = rag_chain.invoke(query)

print(response)
```

# API Reference

## Document Loader

### `NeedleLoader`

A document loader for Needle collections.

- **`__init__(needle_api_key: str, collection_id: str)`**: Initializes the loader.
- **`add_files(files: dict)`**: Adds files to the Needle collection.
- **`load()`**: Loads all documents from the collection.
- **`lazy_load()`**: Lazily loads documents from the collection.


## Retriever

### `NeedleRetriever`

A retriever for fetching documents from Needle collections.

- **`__init__(needle_api_key: str, collection_id: str)`**: Initializes the retriever.
- **`retrieve(query: str)`**: Retrieves documents matching the query.

---

## Chains

- **`create_stuff_documents_chain(llm, prompt)`**: Creates a chain to combine documents into a single response.
- **`create_retrieval_chain(retriever, question_answer_chain)`**: Creates a RAG pipeline combining retrieval and generation.
