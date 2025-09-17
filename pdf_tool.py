

import streamlit as st
import os
from utils import summarizer

def main():
    st.set_page_config(page_title="PDF Summarizer ", layout="centered")
    st.title("📄 PDF Summarizer Tool")
    st.write("Summarize your PDF files in just a few seconds with Gemini")
    st.divider()

    pdf = st.file_uploader("Upload your PDF document", type="pdf")
    # input for Gemini API Key
    gemini_key = st.text_input("Enter your API Key", type="password")

    if st.button("Generate Summary"):
        if pdf is None:
            st.warning("⚠️ Please upload a PDF file.")
        elif not gemini_key:
            st.error("❌ Please provide  API Key.")
        else:
            os.environ["GEMINI_API_KEY"] = gemini_key
            with st.spinner("⏳ Summarizing..."):
                try:
                    summary = summarizer(pdf)
                    st.subheader("📑 Summary")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
