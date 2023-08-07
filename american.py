import requests
from bs4 import BeautifulSoup
import wikipediaapi
from tabulate import tabulate

def get_presidents_data():
    url = "https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        president_table = soup.find("table", class_="wikitable")
        presidents_data = []

        for row in president_table.find_all("tr")[1:]:
            columns = row.find_all("td")
            if len(columns) >= 3:
                name = columns[1].text.strip()
                term = columns[3].text.strip()
                presidents_data.append((name, term))

        return presidents_data
    else:
        print("Failed to fetch data from Wikipedia.")
        return None

def fetch_president_details(name):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(name)
    
    if not page.exists():
        return None, None, None
    
    summary = page.summary
    quotes = [quote.strip() for quote in page.section_by_title("Quotes").text.split('\n') if quote.strip()]
    
    return summary, quotes

def display_presidents_data(presidents_data):
    headers = ["#","Name", "Term", "Summary", "Quotes"]
    table_data = []

    for idx, (name, term) in enumerate(presidents_data, start=1):
        summary, quotes = fetch_president_details(name)
        table_data.append([idx, name, term, summary, "\n".join(quotes)])
        
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    presidents_data = get_presidents_data()
    if presidents_data:
        display_presidents_data(presidents_data)
