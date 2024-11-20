import os
import openai
import chromadb
import requests
from bs4 import BeautifulSoup
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import streamlit as st
from config import URLS_TO_SCRAPE

# Get the OpenAI API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")    
if not openai_api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# Set OpenAI API key
openai.api_key = openai_api_key

# Initialize Chroma DB client
client = chromadb.Client()
collection_name = "school_knowledge"

def get_or_create_collection():
    """Gets or creates a Chroma collection."""
    try:
        collection = client.get_collection(collection_name)
    except Exception as e:
        print(f"Error getting collection: {e}")
        collection = client.create_collection(collection_name)
    return collection

def scrape_website(urls):
    """Scrapes the given URLs and extracts paragraphs of text."""
    all_content = []
    for url in urls:
        try:
            print(f"Scraping URL: {url}")
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            page_content = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
            if page_content:
                all_content.append((url, page_content))
            else:
                print(f"No content found in {url}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return all_content

def add_documents_to_collection(collection, documents):
    """Adds documents to the Chroma DB collection."""
    all_texts = []
    for url, content in documents:
        for para in content:
            all_texts.append({"url": url, "text": para})

    ids = [f"doc_{i + 1}" for i in range(len(all_texts))]
    print(f"Adding {len(all_texts)} documents to Chroma DB...")
    collection.add(documents=[doc["text"] for doc in all_texts], ids=ids,
                   metadatas=[{"url": doc["url"]} for doc in all_texts])

def perform_search(query):
    """Performs a semantic search in Chroma DB."""
    collection = get_or_create_collection()

    if collection.count() == 0:
        # If collection is empty, scrape data and add to the collection
        scraped_content = scrape_website(URLS_TO_SCRAPE)
        add_documents_to_collection(collection, scraped_content)

    # Get all documents and metadata from the collection
    results = collection.get()
    all_docs = results['documents']
    all_metadata = results['metadatas']

    print(f"Found {len(all_docs)} documents in the collection")

    # Use OpenAI's Embedding API for semantic search
    embeddings = openai.Embedding.create(input=all_docs, model="text-embedding-ada-002")['data']
    doc_embeddings = [embedding['embedding'] for embedding in embeddings]

    # Create embedding for the query
    query_embedding = openai.Embedding.create(input=[query], model="text-embedding-ada-002")['data'][0]['embedding']

    # Compute cosine similarity between query and document embeddings
    cosine_sim = cosine_similarity([query_embedding], doc_embeddings)
    best_match_idx = np.argmax(cosine_sim)

    # Get the best matching document
    best_doc = all_docs[best_match_idx]
    best_url = all_metadata[best_match_idx]['url']
    best_score = cosine_sim[0][best_match_idx]

    # Return the top result and highlighted text
    return [(best_score, best_doc, best_url)], highlight_text(best_doc, query)

def highlight_text(text, query):
    """Highlights the query text in the document."""
    return text.replace(query, f"<mark>{query}</mark>")

def summarize_text(text, query):
    """Generates a summary of the text based on the query using OpenAI's GPT-3.5-turbo model."""
    try:
        prompt = f"Summarize the following text based on the query '{query}':\n\n{text}"

        # Using OpenAI's ChatCompletion endpoint for summarization
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7,
        )

        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Error generating summary."

def run_streamlit_app():
    """Runs the Streamlit app for querying the assistant."""
    st.title("School Knowledge Assistant")
    query = st.text_input("Enter your query:")

    if query:
        search_results, highlighted_text = perform_search(query)

        if search_results:
            # Display top result
            st.subheader("Best Match:")
            st.markdown(highlighted_text, unsafe_allow_html=True)

            # Summarize the best match document
            summary = summarize_text(search_results[0][1], query)
            st.subheader("Summary:")
            st.write(summary)

        else:
            st.write("No results found.")

if __name__ == "__main__":
    run_streamlit_app()
