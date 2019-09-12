import requests
from bs4 import BeautifulSoup
from random import randint
from csv import writer

BASE_URL = "http://quotes.toscrape.com"
links = []
all_quotes = []

def scrape_pages():
    next_url = "http://quotes.toscrape.com"
    while True:
        print(f"scraping {next_url}...")
        r = requests.get(next_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        next_page = soup.select(".next")
        if next_page:
            new_url = next_page[0].find("a")["href"]
            links.append(next_url)

            if new_url:
                next_url =  BASE_URL + new_url
            else:
                break
        else:
            break
    #print(links) testing

def scrape_quotes():
    for link in links:
        response = requests.get(link)

        soup = BeautifulSoup(response.text, "html.parser")
        #print(soup)

        quotes = soup.select(".quote")

        for quote in quotes:
            text = quote.find("span")
            author = quote.find("small")
            author_bio = quote.find("a")["href"]
            all_quotes.append([text.get_text(), author.get_text(), author_bio])
    #print(f"{len(all_quotes)} quotes scraped")

def quote_to_csv():
    with open("quotes.csv", "w", encoding="utf-8", newline="") as file:
        csv_writer = writer(file)
        csv_writer.writerow(["Quote Text", "Author", "Bio Link"])
        for quote in all_quotes:
            csv_writer.writerow(quote)

scrape_pages()
scrape_quotes()
quote_to_csv()