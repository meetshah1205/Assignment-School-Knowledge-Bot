import os
from dotenv import load_dotenv
import chromadb
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import streamlit as st
from config import URLS_TO_SCRAPE, HEADERS

class SchoolKnowledgeAssistant:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize OpenAI client
        self.openai_client = OpenAI()  # Will automatically use OPENAI_API_KEY from environment
        
        # Initialize ChromaDB with updated configuration
        persist_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
        os.makedirs(persist_dir, exist_ok=True)
        
        # Initialize ChromaDB client with new PersistentClient
        self.chroma_client = chromadb.PersistentClient(path=persist_dir)
        
        # Initialize embedding function with latest OpenAI embeddings
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables or .env file")
            
        self.embedding_function = chromadb.utils.embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name="text-embedding-3-small"  # Updated to latest OpenAI embedding model
        )
        
        self.collection = self._initialize_collection()

    def _initialize_collection(self):
        """Initialize or retrieve the ChromaDB collection"""
        try:
            collection = self.chroma_client.get_or_create_collection(
                name="school_knowledge",
                embedding_function=self.embedding_function,
                metadata={"description": "School website content"}
            )
            
            if collection.count() == 0:
                print("New collection created, populating with content...")
                self._populate_collection(collection)
            else:
                print(f"Using existing collection with {collection.count()} documents")
                
            return collection
            
        except Exception as e:
            print(f"Error initializing collection: {e}")
            raise

    def _scrape_content(self):
        """Scrape content from configured URLs"""
        content = []
        for url in URLS_TO_SCRAPE:
            try:
                response = requests.get(url, headers=HEADERS, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                content_elements = soup.find_all(['p', 'div', 'article', 'section'])
                
                page_content = []
                for el in content_elements:
                    text = el.get_text().strip()
                    if (len(text) > 50 and 
                        not any(x in text.lower() for x in ['copyright', 'all rights reserved', 'cookie', 'privacy policy']) and
                        not el.find_parent(['header', 'footer', 'nav'])):
                        page_content.append(text)
                
                if page_content:
                    content.extend([{
                        "text": para,
                        "url": url,
                        "id": f"{url.split('/')[-1]}_{len(content) + i}"
                    } for i, para in enumerate(page_content)])
                    print(f"Scraped {len(page_content)} sections from {url}")
                    
            except requests.RequestException as e:
                print(f"Error scraping {url}: {e}")
                continue
                
        return content

    def _populate_collection(self, collection):
        """Populate the collection with scraped content"""
        content = self._scrape_content()
        
        if not content:
            raise ValueError("No content was scraped from the configured URLs")
        
        try:
            batch_size = 50
            for i in range(0, len(content), batch_size):
                batch = content[i:i + batch_size]
                try:
                    collection.add(  # Changed from upsert to add as per latest ChromaDB
                        documents=[item["text"] for item in batch],
                        ids=[item["id"] for item in batch],
                        metadatas=[{"url": item["url"]} for item in batch]
                    )
                except Exception as e:
                    print(f"Error adding batch {i//batch_size}: {e}")
                    continue
            print(f"Successfully added {collection.count()} documents to collection")
        except Exception as e:
            print(f"Error adding documents to collection: {e}")
            raise

    def query(self, user_query: str, n_results: int = 3):
        """Query the collection and return relevant results"""
        if not user_query.strip():
            return []
            
        try:
            results = self.collection.query(
                query_texts=[user_query],
                n_results=n_results
            )
            
            matches = []
            if results and results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    matches.append({
                        'text': results['documents'][0][i],
                        'url': results['metadatas'][0][i]['url'],
                        'distance': results['distances'][0][i] if results.get('distances') else None
                    })
            
            return matches
            
        except Exception as e:
            print(f"Error querying collection: {e}")
            return []

    def generate_summary(self, text: str, query: str) -> str:
        """Generate a summary using OpenAI's GPT model"""
        if not text or not query:
            return "Invalid input for summary generation."
            
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can also use "gpt-4" if available
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for a school. Provide concise, relevant summaries focused on the query context."},
                    {"role": "user", "content": f"Summarize this text in the context of the query '{query}':\n\n{text}"}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Unable to generate summary due to an error."

def create_streamlit_interface():
    """Create the Streamlit user interface"""
    st.set_page_config(
        page_title="School Knowledge Assistant",
        page_icon="🏫",
        layout="wide"
    )
    
    st.title("🏫 School Knowledge Assistant")
    
    @st.cache_resource(show_spinner=False)
    def get_assistant():
        try:
            with st.spinner('Initializing the knowledge assistant...'):
                return SchoolKnowledgeAssistant()
        except Exception as e:
            st.error(f"Failed to initialize assistant: {str(e)}")
            return None
    
    assistant = get_assistant()
    
    if assistant:
        query = st.text_input(
            "Enter your query about the school:",
            placeholder="e.g., What are the school's admission requirements?"
        )
        
        if query:
            with st.spinner('Searching for relevant information...'):
                results = assistant.query(query)
                
                if results:
                    for i, result in enumerate(results):
                        with st.container():
                            st.subheader(f"Result {i+1}")
                            st.info(result['text'])
                            st.markdown(f"📍 Source: [{result['url']}]({result['url']})")
                            
                            if result.get('distance') is not None:
                                similarity = max(0, min(100, (1 - result['distance']) * 100))
                                st.progress(similarity / 100, text=f"Relevance: {similarity:.1f}%")
                            
                            with st.spinner('Generating summary...'):
                                summary = assistant.generate_summary(result['text'], query)
                                st.subheader("Summary")
                                st.success(summary)
                            
                            st.divider()
                else:
                    st.warning("No relevant information found. Try rephrasing your query.")
    else:
        st.error("The assistant is not available. Please check the application logs.")

if __name__ == "__main__":
    create_streamlit_interface()