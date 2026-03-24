import os
from pdfreader import read_pdf
from chunker import chunk_pages
from embedder import embed_chunks
from vectorstore import store_in_pinecone
import glob

def run():
    pdf_files = glob.glob("./resources/*.pdf")

    if not pdf_files:
        print("No PDF files found in ./resources/")
        return

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path}")
        source = os.path.splitext(os.path.basename(pdf_path))[0]
        pages = read_pdf(pdf_path)
        chunks = chunk_pages(pages, chunk_size=900, chunk_overlap=150)
        embedded_chunks = embed_chunks(chunks)
        store_in_pinecone(chunks, embedded_chunks, namespace="", source=source)
        print(f"Done: {pdf_path} — {len(chunks)} chunks")

if __name__ == "__main__":
    run()