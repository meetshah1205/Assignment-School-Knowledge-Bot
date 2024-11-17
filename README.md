# 🎓 School Knowledge Assistant 📚

Welcome to the **School Knowledge Assistant**! This app allows you to query various topics from the **Shree Vidyanagar School** website. Using **natural language processing** and **fuzzy search**, the assistant provides relevant pages from the school’s website, highlighting key information to help you find what you're looking for! 🚀

---

## 🛠️ How to Install

1. **Clone the repository**:
```bash
   git clone https://github.com/meetshah1205/Assignment-School-Knowledge-Bot.git # clone the repository
```

2. **Create and activate a virtual environment (optional but recommended):**
```bash
  python -m venv venv
  # On Windows
  venv\Scripts\activate
  # On MacOS/Linux
  source venv/bin/activate 
```

3. **Set the OpenAi API key as the environment variable:**
```bash
set OPENAI_API_KEY=sk-proj-your_api-key_here # Windows (Run in a CMD session because Powershell doesn't work for some 
reason)
export OPENAI_API_KEY=sk-proj-your_api-key_here # MacOS/Linux
 
```
3.1 ***Verify if the environment variable is set:***
```bash
echo %OPENAI_API_KEY% # Windows
echo $OPENAI_API_KEY # MacOS/Linux
```

4. **Install the dependencies:**
```bash
  pip install -r requirements.txt 
```

5. **Run the app:**
```bash
  streamlit run school_scraper.py 
```
Now you're ready to use the app in your browser! 🖥️

<hr>

## 🧑‍💻 How to Use
1. **Open the app in your browser 🌐**: After running the above command, open your browser and go to 
   [http://localhost:8501](http://localhost:8501).
2. **Enter a query 🔍**: Type any keyword or phrase related to your query, like "English Message" or "Admission 
   Procedure". The assistant will use fuzzy search to find the most relevant results! 🧠✨.
3. **View the Results 📄**: The app will show the top relevant result with a dropdown to select from multiple options.
   The best match will also have highlighted text showing where your query was found on the page. 🎯

<hr>

## 📦 Technologies Used
- ChromaDB: For managing and retrieving documents efficiently 🗂️
- Streamlit: For creating a user-friendly interface 💻
- BeautifulSoup: For scraping content from web pages 🌍
- Fuzzywuzzy: For fuzzy string matching to find the closest match 🔍
- Requests: To fetch the content from URLs 🌐
- OpenAI: To process and display the results in a summarized fasshion
<hr>

## 🔧 Features
- Fuzzy Search: Get the most relevant results from the school’s website even if the query is not an exact match! 💡
- Interactive Dropdown: Choose from multiple answers for better flexibility and ease of use. 🛠️
- Highlights: View the highlighted part of the page where the query was found. ✨
- Ai: Summarizes the text of the page to display to the point answers

<hr>

## 🤖 Contributions
Feel free to contribute! Open an issue or a pull request, and we'll get back to you. 📝(if i have the motivation to 
do that bcuz i will probably not even look at it again)

<hr>

## 📝 Note
This app is for educational purposes and is built to demonstrate web scraping and fuzzy search techniques using a real-world school website. 🏫

<hr>

## 🖼️ Visual representation of this project
Here is a very very high quality art of the visual representation of this project:
![image](how-this-works.png)

<hr>

Have fun exploring! 🚀
