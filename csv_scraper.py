import requests
from bs4 import BeautifulSoup
from random import randint
from csv import writer

#home url for scraping
BASE_URL = "http://quotes.toscrape.com"
links = []
#This will have nested lists of quotes, author, link
all_quotes = []

def scrape_pages():
    #this url will use the base and the next page link to loop through all pages
    next_url = "http://quotes.toscrape.com"
    #get all page links and add to links list
    while True:
        print(f"scraping {next_url}...")
        #gets the url as a request
        r = requests.get(next_url)
        #parse into html
        soup = BeautifulSoup(r.content, 'html.parser')
        #check for next button link
        next_page = soup.select(".next")
        #if there is a next button
        if next_page:
            #get next button link
            new_url = next_page[0].find("a")["href"]
            #add link to list.
            links.append(next_url)

            #if there is a link
            if new_url:
                next_url =  BASE_URL + new_url
            else:
                break
        else:
            break
    #print(links) testing

def scrape_quotes():
    for link in links:
        #create our request object
        response = requests.get(link)

        #instantiate bs4 and create a parsed object this will be able to give use the html as text
        soup = BeautifulSoup(response.text, "html.parser")
        #print(soup)

        #select all divs with the class=quote
        quotes = soup.select(".quote")

            #scrape each quote pull out the quote, author  and link to author bio
        for quote in quotes:
            text = quote.find("span")
            author = quote.find("small")
            #use find over find_all so we only get the first anchor tag for each quote div
            author_bio = quote.find("a")["href"]
            all_quotes.append([text.get_text(), author.get_text(), author_bio])
    #print(f"{len(all_quotes)} quotes scraped")

def quote_to_csv():
    #write quotes to CSV
    with open("quotes.csv", "w", encoding="utf-8", newline="") as file:
        csv_writer = writer(file)
        csv_writer.writerow(["Quote Text", "Author", "Bio Link"])
        for quote in all_quotes:
            csv_writer.writerow(quote)

scrape_pages()
scrape_quotes()
quote_to_csv()