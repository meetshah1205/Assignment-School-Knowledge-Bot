from bs4 import BeautifulSoup
import requests
import config  # Importing the config file


def scrape_school_website():
    response = requests.get(config.SCHOOL_WEBSITE_URL, headers=config.HEADERS)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove unwanted tags
        for unwanted in soup(['script', 'style', 'footer', 'header', 'nav']):
            unwanted.decompose()

        # Filter and clean text content
        text_content = []
        for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            line = element.get_text(strip=True)
            if line:
                text_content.append(line)

        return "\n\n".join(text_content)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None


# Example usage
if __name__ == "__main__":
    text_content = scrape_school_website()
    if text_content:
        print(text_content[:1000])  # Print first 1000 characters for preview
