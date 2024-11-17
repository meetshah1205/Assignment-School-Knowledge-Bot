# School Knowledge Assistant

The **School Knowledge Assistant** is an interactive web application that helps users get quick, AI-generated answers based on the content scraped from the official school website. Powered by OpenAI's language models, this assistant responds to user queries in real-time, providing accurate information sourced directly from the school's web pages.

## Features

- **Direct AI Interaction**: Users can directly input queries related to the school, and the AI provides answers based on the scraped data from the official website.
- **Real-time Responses**: AI answers are generated based on scraped content, providing relevant and accurate information to users.
- **Chat-like Interface**: The text input box is placed at the bottom of the page, mimicking a chatbot-like experience, similar to platforms like [ChatGPT](https://chat.openai.com).
- **Searchable Topics**: Available school topics are listed, allowing users to explore different sections, such as "Admission Procedure", "Vision & Mission", and "Infrastructure".
- **Flexible**: Can easily be expanded to handle new pages and content for additional topics.

## Installation

To run this application locally, follow the steps below:

### Prerequisites
Ensure you have Python 3.7+ installed. You can download Python from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/).

### Step 1: Clone the repository
```bash
git clone https://github.com/your-username/school-knowledge-assistant.git
cd school-knowledge-assistant # The directory name can be different so just cd to whatever the name of the directory is
```

### Step 2: Set up a virtual environment (optional but recommended)
```bash
python -m venv venv
```
Activate the virtual environment:
- On ~bloatware warehouse~ Windows:
  ```bash
  venv\Scripts\activate
  ```
- On MacOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```
- Or you can install them separately:
```bash
pip install streamlit  # For GUI
pip install chromadb  # For context-based searching
pip install requests  # For making HTTP requests
pip install beautifulsoup4  # For web scraping
pip install pandas  # For handling tabular data
pip install numpy  # For numerical operations
pip install fuzzywuzzy  # For string similarity matching
pip install python-Levenshtein  # Optimizes fuzzywuzzy's performance
pip install sentence-transformers  # For embedding-based operations
pip install openai # For the Ai part
```

### Step 4: Set up API Keys
- In Windows:
  - Open Command Prompt (CMD or cmd.exe).
  - `cd` into the project folder (if not already).
  - Run the following command
    ```bash
    set OPENAI_API_KEY=sk-proj-your-api-key-here
    ```
    (Replace `sk-proj-your_api-key_here` with you actual OpenAi API key.)
    
- In MacOS/Linux:
     - Open terminal.
     - `cd` into the project folder (If not already).
     - Run the following command
       ```bash
       export OPENAI_API_KEY='sk-proj-your-api-key-here'
       ```
       (Replace `sk-proj-your_api-key_here` with you actual OpenAi API key.)

   #### Step 4.1: Verify the setting of environment variables:
  In the same CMD or terminal session run the following commnad:
   - Windows (CMD):
      ```bash
     echo %OPENAI_API_KEY%
     ```
  - MacOS/Linux (Terminal):
    ```bash
    echo $OPENAI_API_KEY
    ```

   ### Step 5: Run the Applicatio
     Run the following command in the same CMD or Terminal session:
   ```bash
    streamlit run school_scraper.py
    ```

     It should automatically open a browser instance or a new tab in already open browser. But if does not go to [http://localhost:8501](http://localhost:8501).

## Usage
1. Once the app is running, you'll see an input field at the bottom of the page.
2. Type any query related to the school (e.g., "What is the admission procedure?") and hit Enter.
3. The AI will process your query and respond with the information sourced from the school website.
4. You can also explore different topics like "Infrastructure" or "Vision & Mission" through the available options.

## Technologies used
- Streamlit: Used for building the interactive web interface.
- OpenAI API: For processing and generating natural language responses.
- BeautifulSoup: For scraping content from the school website.
- Requests: For fetching web content from the school's website.
- Python: Main programming language.

## Future Enhancements
- Expand the AI's ability to summarize content dynamically, making it more responsive and precise.
- Add more topics from the school website for a richer user experience.
- Improve the search functionality to allow more refined queries and better results.
- Include a more detailed feedback mechanism for users to report incorrect or incomplete information.

  
