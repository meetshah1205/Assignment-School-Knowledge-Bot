import requests
from bs4 import BeautifulSoup
import config


def display_topics():
    """Display available topics to the user."""
    print("Available Topics to Scrape:")
    for index, (topic, _) in enumerate(config.TOPICS.items(), start=1):
        print(f"{index}. {topic}")


def get_user_choice():
    """Prompt the user to select a topic by index."""
    while True:
        try:
            choice = int(input("Enter the number of the topic you want to scrape: "))
            if 1 <= choice <= len(config.TOPICS):
                return choice - 1  # Convert to 0-based index for list
            else:
                print("Invalid choice. Please choose a valid number.")
        except ValueError:
            print("Please enter a valid number.")


def scrape_page(url):
    """Scrape and return the text content from the given URL."""

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove unwanted elements (e.g., script, style, footer)
            for unwanted in soup(['script', 'style', 'footer', 'header', 'nav']):
                unwanted.decompose()

            # Extract relevant text
            content = []
            for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                text = element.get_text(strip=True)
                if text:
                    content.append(text)

            return content
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred while trying to scrape the page: {e}")
        return None
    except requests.RequestException as e:
        print(f"An error occurred while trying to scrape the page: {e}")
        return None


def save_scraped_data(topic, content):
    """Save the scraped data to a file."""
    filename = f"scraped_{topic.replace(' ', '_')}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Scraped Data for Topic: {topic}\n")
        file.write("=" * 50 + "\n")
        for i, chunk in enumerate(content):
            file.write(f"Chunk {i + 1}:\n")
            file.write(f"{chunk}\n")
            file.write("-" * 50 + "\n")
        print(f"Data has been saved to {filename}")


def main():
    """Main function to run the program."""
    display_topics()

    # Get the user's choice
    choice = get_user_choice()

    # Get the selected topic name and URL
    selected_topic = list(config.TOPICS.keys())[choice]
    selected_url = config.TOPICS[selected_topic]

    # Scrape the content from the selected URL
    content = scrape_page(selected_url)

    if content:
        save_scraped_data(selected_topic, content)
    else:
        print("No content was retrieved from the selected page.")


if __name__ == "__main__":
    main()
