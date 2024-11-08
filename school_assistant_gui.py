import streamlit as st
import json


# Load the scraped content from the JSON file
def load_scraped_content():
    try:
        with open("scraped_content.json", "r", encoding="utf-8") as json_file:
            content = json.load(json_file)
        return content
    except FileNotFoundError:
        st.error("No scraped data found. Please scrape the website first!")
        return {}


# Search for content matching the query
def search_content(query, all_content):
    """Searches through the available content for the most relevant match."""
    query = query.lower()

    for topic, content in all_content.items():
        if query in content.lower():
            return topic, content

    best_match = None
    highest_score = 0

    for topic, content in all_content.items():
        content_clean = content.lower()
        score = sum(content_clean.count(word) for word in query.split())

        if score > highest_score:
            best_match = topic
            highest_score = score

    return best_match, all_content.get(best_match) if best_match else (None, None)


# Streamlit app layout
def main():
    st.title("School Knowledge Assistant")

    # Load scraped content
    all_content = load_scraped_content()

    if all_content:
        st.sidebar.header("Search")
        query = st.sidebar.text_input("Enter a keyword to search:")

        if query:
            matched_topic, matched_content = search_content(query, all_content)

            if matched_topic and matched_content:
                st.subheader(f"Matched Topic: {matched_topic}")
                st.write(matched_content)
            else:
                st.warning("No relevant content found. Please try again with a different keyword.")
        else:
            st.sidebar.info("Enter a keyword to search for relevant content.")


if __name__ == "__main__":
    main()
