import requests
from bs4 import BeautifulSoup
import config
import string
import re

def scrape_school_website(url):
    """Fetches and cleans content from a given URL."""
    try:
        response = requests.get(url, headers=config.HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove unnecessary tags
        for unwanted in soup(['script', 'style', 'footer', 'header', 'nav']):
            unwanted.decompose()

        # Extract text content from heading and paragraph tags
        text_content = []
        for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            line = element.get_text(strip=True)
            if line:
                text_content.append(line)

        return "\n\n".join(text_content)
    except requests.exceptions.Timeout:
        print("Request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the page. Error: {e}")
    return None

def get_all_content():
    """Scrapes all topics and returns a dictionary with content for each topic."""
    all_content = {}
    for topic, url in config.TOPICS.items():
        content = scrape_school_website(url)
        if content:
            all_content[topic] = content
        else:
            print(f"Failed to scrape content for: {topic}")
    return all_content
