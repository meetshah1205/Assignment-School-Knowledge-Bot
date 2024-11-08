import re
import requests
from bs4 import BeautifulSoup
import datetime
import config
import string


def scrape_school_website(url):
    """Fetches and cleans content from a given URL."""
    try:
        response = requests.get(url, headers=config.HEADERS, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
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
        print("Request timed out. Please try again later.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the page. Error: {e}")
    return None


def clean_text(text):
    """Cleans and normalizes the input text for easier comparison."""
    # Normalize: lower case, remove punctuation, and unnecessary spaces
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def save_to_file(content, topic_name):
    """Saves the formatted content to a timestamped text file."""
    filename = f"{topic_name}_{datetime.datetime.now():%Y%m%d_%H%M%S}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Content saved to {filename}")


def display_topics():
    """Displays a list of topics available for scraping."""
    print("Available Topics to Scrape:")
    for i, topic in enumerate(config.TOPICS, start=1):
        print(f"{i}. {topic}")


def search_content(query, all_content):
    """Searches through the available content for the most relevant match."""
    query = clean_text(query)  # Normalize user input

    # Check for exact matches first
    for topic, content in all_content.items():
        if query in content:
            return topic, content

    # If no exact match, find the most relevant match
    best_match = None
    highest_score = 0

    for topic, content in all_content.items():
        # Compute a simple relevance score based on the occurrence of query terms
        content_clean = clean_text(content)
        score = sum(content_clean.count(word) for word in query.split())

        if score > highest_score:
            best_match = topic
            highest_score = score

    return best_match, all_content[best_match]


def main():
    # Scrape all pages first and store the content
    all_content = {}
    for topic, url in config.TOPICS.items():
        content = scrape_school_website(url)
        if content:
            all_content[topic] = content
        else:
            print(f"Failed to scrape content for: {topic}")

    # Display available topics and get user input
    display_topics()
    user_input = input("Enter the topic you want to search: ")

    # Search for the most relevant topic
    matched_topic, matched_content = search_content(user_input, all_content)

    # Save the matched content to file
    if matched_topic:
        print(f"\nMatched Topic: {matched_topic}")
        save_to_file(matched_content, matched_topic)
    else:
        print("No relevant topic found. Please try again with a different query.")


if __name__ == "__main__":
    main()
