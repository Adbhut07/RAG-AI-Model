from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import glob
import os
import shutil
import re

# Configuration
PDF_DIR = "./pdfs"
DB_LOCATION = "./chroma_langchain_db_pdf"
COLLECTION_NAME = "protocols_docs"


def clean_text(text):
    """Clean and normalize text content"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_section_title(text):
    """Try to extract section title from the start of the text"""
    match = re.search(r'^(\d+(?:\.\d+)*\s+.+?)(?=\.|\n|$)', text.strip())
    return match.group(1).strip() if match else "Unknown Section"


def load_and_process_documents():
    """Load PDFs and process them into structured, section-based chunks"""
    pdf_paths = glob.glob(os.path.join(PDF_DIR, "*.pdf"))

    if not pdf_paths:
        print(f"No PDF files found in {PDF_DIR}")
        return []

    print(f"Found {len(pdf_paths)} PDF files:")
    for path in pdf_paths:
        print(f"  - {os.path.basename(path)}")

    all_documents = []

    for path in pdf_paths:
        try:
            print(f"Loading: {os.path.basename(path)}")
            loader = PyMuPDFLoader(path)
            docs = loader.load()

            for doc in docs:
                text = clean_text(doc.page_content)
                if len(text) < 50:
                    continue

                doc.page_content = text
                doc.metadata["source"] = os.path.basename(path)
                doc.metadata["page_number"] = doc.metadata.get("page", -1)
                doc.metadata["section_title"] = extract_section_title(text)

                all_documents.append(doc)

            print(f"  Loaded {len(docs)} pages")

        except Exception as e:
            print(f"Error loading {path}: {str(e)}")

    print(f"Total documents loaded: {len(all_documents)}")

    # Section-aware text splitting
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    split_docs = text_splitter.split_documents(all_documents)
    print(f"Documents split into {len(split_docs)} chunks")

    return split_docs


def setup_vector_store(force_rebuild=False):
    """Setup vector store with embeddings and structured chunks"""

    if force_rebuild and os.path.exists(DB_LOCATION):
        print("Removing existing database...")
        shutil.rmtree(DB_LOCATION)

    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    db_exists = os.path.exists(DB_LOCATION)

    if not db_exists:
        print("Database doesn't exist. Creating new vector store...")
        documents = load_and_process_documents()

        if not documents:
            print("No documents to process!")
            return None

        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=DB_LOCATION,
            embedding_function=embeddings
        )

        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            ids = [f"doc_{i + j}" for j in range(len(batch))]
            print(f"Adding batch {i // batch_size + 1}/{(len(documents) - 1) // batch_size + 1}")
            vector_store.add_documents(documents=batch, ids=ids)

        print("Vector store created successfully!")

    else:
        print("Loading existing vector store...")
        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=DB_LOCATION,
            embedding_function=embeddings
        )

    return vector_store


def test_retrieval(retriever, test_queries=None):
    if test_queries is None:
        test_queries = [
            "What is the RAP format in eUSB2?",
            "How does L2 suspend work in repeater mode?",
            "What are the electrical requirements for high-speed signaling?",
            "Explain the eUSB2 state machine"
        ]

    print("\n" + "=" * 50)
    print("TESTING RETRIEVAL SYSTEM")
    print("=" * 50)

    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 30)
        try:
            docs = retriever.invoke(query)
            print(f"Retrieved {len(docs)} documents:")
            for i, doc in enumerate(docs):
                source = doc.metadata.get('source', 'Unknown')
                section = doc.metadata.get('section_title', 'Unknown Section')
                content_preview = doc.page_content[:200].replace('\n', ' ')
                print(f"  {i + 1}. Source: {source}, Section: {section}")
                print(f"     Content: {content_preview}...")
        except Exception as e:
            print(f"Error: {str(e)}")


print("Initializing RAG system...")
vector_store = setup_vector_store(force_rebuild=False)

if vector_store is None:
    print("Failed to initialize vector store!")
    retriever = None
else:
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 8, "fetch_k": 30, "lambda_mult": 0.7}
    )
    print("RAG system initialized successfully!")

    # Uncomment to test
    # test_retrieval(retriever)
