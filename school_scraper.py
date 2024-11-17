import openai
import requests
from bs4 import BeautifulSoup
import config
import streamlit as st


# Function to fetch and process content from the provided URL
def fetch_and_process_content(url):
    try:
        # Fetch the webpage content
        response = requests.get(url, headers=config.HEADERS)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all the text from the page, ignoring scripts and styles
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()
        text = soup.get_text(separator=' ', strip=True)

        return text
    except Exception as e:
        return f"Error fetching content: {str(e)}"


# Function to summarize content using OpenAI API based on scraped data
def generate_response(query, scraped_data):
    prompt = f"""
    You are a helpful assistant. Given the following content about a school website, answer the user's query as accurately as possible. If you think the content might be incorrect or incomplete, offer alternative options or ask the user to clarify.

    Content:
    {scraped_data}

    User Query: {query}

    Response:
    """
    try:
        # OpenAI Chat API (for GPT-3.5 or GPT-4)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can also use "gpt-4" if you prefer
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )

        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"


# Streamlit app layout
def main():
    st.title("School Knowledge Assistant")
    st.markdown("### Ask anything related to the school and get an answer.")

    # Fetch and process content for scraping
    school_url = config.TOPICS['Home']  # We can default to the home page or a relevant page
    scraped_content = fetch_and_process_content(school_url)

    # Display prompt input at the bottom, like ChatGPT's input box
    st.markdown("<hr>", unsafe_allow_html=True)  # A divider line
    user_input = st.text_input("Type your question here...", "")

    # Display response area
    if user_input:
        st.markdown("### AI's Answer:")

        # Generate AI response based on the user's input and scraped data
        response = generate_response(user_input, scraped_content)
        st.write(response)

    # Additional Options or Topics for the User
    st.markdown("### Other Topics:")
    for topic in config.TOPICS:
        st.write(f"- {topic}")


if __name__ == "__main__":
    main()
