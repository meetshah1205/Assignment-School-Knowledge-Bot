import streamlit as st
import sqlite3
from fuzzywuzzy import fuzz
from config import SCHOOL_WEBSITE_URL  # Assuming you're importing the URL from config.py
from school_scraper import scrape_school_website  # Assuming scrape_schools is already implemented

# Function to search for exact and fuzzy matches
def search_in_db(query, exact_match=True, threshold=80):
    """Search for a query in the database with exact or fuzzy match."""
    conn = sqlite3.connect('school_data.db')
    c = conn.cursor()

    c.execute("SELECT * FROM schools")
    schools = c.fetchall()
    
    results = []
    
    for school in schools:
        topic = school[1].lower()
        content = school[2].lower()
        query_lower = query.lower()
        
        # Exact match search
        if exact_match:
            if query_lower == topic or query_lower == content:
                results.append(school)
        else:
            # Fuzzy match search
            if fuzz.partial_ratio(query_lower, topic) >= threshold or fuzz.partial_ratio(query_lower, content) >= threshold:
                results.append(school)

    conn.close()
    return results

# Create a function to display the scraped school information
def display_school_info():
    # Connect to the database to get any existing data
    conn = sqlite3.connect('school_data.db')
    c = conn.cursor()

    c.execute("SELECT * FROM schools")
    schools = c.fetchall()

    if len(schools) == 0:
        st.write("No data found.")
    else:
        for school in schools:
            st.write(f"School Name: {school[1]}")
            st.write(f"School Description: {school[2]}")
            st.write("---")

    conn.close()

# Set up the Streamlit interface
st.title("School Assistant")

# Display options for the user
option = st.selectbox(
    "Choose an action",
    ("Scrape School Data", "View School Data", "Search School Data")
)

if option == "Scrape School Data":
    st.write("Starting the scraping process...")

    try:
        # Scrape the data from the website
        scrape_school_website(SCHOOL_WEBSITE_URL)
        st.success("Scraping completed successfully!")
    except Exception as e:
        st.error(f"Error during scraping: {e}")

elif option == "View School Data":
    st.write("Displaying all scraped school data:")
    display_school_info()

elif option == "Search School Data":
    st.write("Search for school data:")
    
    # Input for search query
    query = st.text_input("Enter search query:")
    
    # Checkbox for fuzzy match option
    fuzzy_search = st.checkbox("Enable fuzzy search")
    
    if query:
        if fuzzy_search:
            st.write("Searching with fuzzy match...")
            results = search_in_db(query, exact_match=False, threshold=80)
        else:
            st.write("Searching with exact match...")
            results = search_in_db(query, exact_match=True)
        
        if results:
            for result in results:
                st.write(f"Topic: {result[1]}")
                st.write(f"Content: {result[2]}")
                st.write("---")
        else:
            st.write("No results found.")
