# Module imports
import re
import requests
from bs4 import BeautifulSoup

# File imports
import config  # config.py for storing constants like URLs and headers


def scrape_school_website():
    """
    Fetches the website HTML, removes unwanted tags, and extracts relevant text content.
    Returns cleaned text if successful, or None if the request fails.
    """
    response = requests.get(config.SCHOOL_WEBSITE_URL, headers=config.HEADERS)

    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove unwanted tags because I don't want unnecessary styling and javascript in our output
    for tag in soup(['script', 'style', 'footer', 'header', 'nav']):
        tag.decompose()

    # Extract and clean text content from headings and paragraphs
    text_content = [
        element.get_text(strip=True) for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if element.get_text(strip=True)
    ]

    return "\n\n".join(text_content)


def clean_text(text):
    """
    Cleans the input text by removing unwanted whitespace and special characters.
    Splits text into sections for readability and returns the cleaned text.
    """
    # Replace multiple spaces or newlines with a single space
    text = re.sub(r'\s+', ' ', text)

    # Remove special characters except for basic punctuation
    text = re.sub(r'[^\w\s.,;!?]', '', text)

    # Split text into logical sections
    sections = text.split('\n\n')
    cleaned_sections = [section.strip() for section in sections if section.strip()]

    return "\n\n".join(cleaned_sections)


def chunk_text(text, chunk_size=1000, overlap=200):
    """
    Divides the text into chunks of specified size with optional overlap.
    Returns a list of text chunks.
    """
    words = text.split()
    chunks = [
        " ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size - overlap)
    ]

    return chunks


def process_text_for_embeddings(text):
    """
    Cleans and chunks the provided text for embedding preparation.
    Returns a list of text chunks ready for embeddings.
    """
    cleaned_text = clean_text(text)
    text_chunks = chunk_text(cleaned_text)
    return text_chunks


# Example usage
if __name__ == "__main__":
    # Scrape and process the school website content
    scraped_text = scrape_school_website()

    if scraped_text:
        processed_chunks = process_text_for_embeddings(scraped_text)

        # Preview the first 3 chunks
        for i, chunk in enumerate(processed_chunks[:3]):
            print(f"Chunk {i + 1}:\n{chunk}\n{'-' * 40}")
