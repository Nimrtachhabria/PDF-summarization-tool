PDF Summarization tool

This is a simple Streamlit web app that allows you to upload a PDF and get a summarized version of its content using Google Gemini API.

It uses LangChain, FAISS, and HuggingFace embeddings to process the PDF, then sends the processed context to Gemini for summarization.

🚀 Features

Upload any PDF file.

Extract text from all pages.

Split text into chunks for better processing.

Generate embeddings with HuggingFace (all-MiniLM-L6-v2).

Store/retrieve using FAISS vector database.

Use Gemini API to generate a concise summary in 3–5 sentences.

Clean Streamlit UI.
