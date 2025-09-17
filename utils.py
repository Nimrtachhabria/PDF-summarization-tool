
# import libraries
import os
from pypdf import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS 

# Gemini SDK imports
from google import genai
from google.genai import types as genai_types

def process_text(text):
    """Splits text into chunks and builds a vector store (FAISS)."""
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = splitter.split_text(text)
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    # use FAISS or other vector store
    knowledgeBase = FAISS.from_texts(chunks, embeddings)
    return knowledgeBase

def summarizer(pdf):
    """Summarize the PDF content using Gemini API."""
    if pdf is None:
        return "No PDF file provided."

    # read PDF
    reader = PdfReader(pdf)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() or ""

    # build knowledge base
    kb = process_text(full_text)

    # define query
    query = "Summarize the content of the uploaded PDF file in approximately 3-5 sentences."

    # perform similarity search
    docs = kb.similarity_search(query)

    # configure Gemini
    # make sure you have set environment variable GEMINI_API_KEY
    # or replace os.getenv(...) with your key (not recommended for production)
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    if not gemini_key:
        return "Error: GEMINI_API_KEY not set."

    client = genai.Client(api_key=gemini_key)

    # build content from docs to feed to Gemini prompt
    # you can combine doc texts. Example: join first few docs
    context_text = "\n\n".join([doc.page_content for doc in docs[:3]])

    # call Gemini generate_content
    response = client.models.generate_content(
        model="gemini-1.5-flash",  # or another model you have access to
        contents=f"Here is some context:\n{context_text}\n\nNow summarize this: {query}",
        config=genai_types.GenerateContentConfig(
            temperature=0.7,
            top_p=0.95,
            top_k=0,
            max_output_tokens=512
        )
    )

    return response.text
