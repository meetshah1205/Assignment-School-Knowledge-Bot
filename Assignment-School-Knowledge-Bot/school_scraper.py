import re
import chromadb
import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from bs4 import BeautifulSoup
import streamlit as st
from config import URLS_TO_SCRAPE, HEADERS, TOPICS  # Import URLs and headers from config.py

client = chromadb.Client()
collection_name = "school_knowledge"


def get_or_create_collection():
    try:
        collection = client.get_collection(collection_name)
    except Exception:
        collection = client.create_collection(collection_name)
    return collection


def scrape_website(urls):
    all_content = []  # List to store content
    for url in urls:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        page_content = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
        all_content.append((url, page_content))  # Store the URL along with content
    return all_content


def add_documents_to_collection(collection, documents):
    # Flatten list of documents, using the page URL as ID
    all_texts = []
    for url, content in documents:
        for para in content:
            all_texts.append({"url": url, "text": para})

    ids = [f"doc_{i + 1}" for i in range(len(all_texts))]
    collection.add(documents=[doc["text"] for doc in all_texts], ids=ids,
                   metadatas=[{"url": doc["url"]} for doc in all_texts])


def perform_search(query):
    collection = get_or_create_collection()

    if collection.count() == 0:
        # If collection is empty, scrape data and add to the collection
        scraped_content = scrape_website(URLS_TO_SCRAPE)
        add_documents_to_collection(collection, scraped_content)

    # Get all documents and metadata
    results = collection.get()
    all_docs = results['documents']
    all_metadata = results['metadatas']

    # Perform fuzzy search with better ranking
    search_results = []
    for idx, doc in enumerate(all_docs):
        score = fuzz.partial_ratio(query.lower(), doc.lower())
        if score > 50:  # Minimum threshold for relevance
            search_results.append((score, doc, all_metadata[idx]['url']))

    # Sort results by the score
    search_results.sort(reverse=True, key=lambda x: x[0])

    # Show the best result
    best_match = search_results[0] if search_results else None
    highlighted_text = None
    if best_match:
        best_score, best_doc, best_url = best_match
        highlighted_text = highlight_text(best_doc, query)

    return search_results, highlighted_text


def highlight_text(text, query):
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(r"<mark>\g<0></mark>", text)


def run_streamlit_app():
    st.title("School Knowledge Assistant")
    query = st.text_input("Enter your query:")

    if query:
        search_results, highlighted_text = perform_search(query)

        if search_results:
            # Display top result
            st.subheader("Best Match:")
            st.markdown(highlighted_text, unsafe_allow_html=True)

            # Create dropdown to select from other results
            if len(search_results) > 1:
                st.subheader("Other Relevant Results:")
                options = [f"Result {i + 1}" for i in range(1, len(search_results))]
                selected_option = st.selectbox("Select a result:", options)

                # Highlight the selected document
                selected_index = options.index(selected_option) + 1  # Index of the selected option
                score, selected_doc, selected_url = search_results[selected_index]
                st.write(f"**Score**: {score}")
                st.write(f"**Source URL**: {selected_url}")
                st.markdown(highlight_text(selected_doc, query), unsafe_allow_html=True)

        else:
            st.write("No results found.")


if __name__ == "__main__":
    run_streamlit_app()
