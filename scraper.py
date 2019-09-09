import requests
from bs4 import BeautifulSoup
from random import randint

#home url for scraping
base_url = "http://quotes.toscrape.com"
#this url will use the base and the next page link to loop through all pages
next_url = "http://quotes.toscrape.com"

links = []

#This will have nested lists of quotes, author, link
all_quotes = []

#get all page links and add to links list
while True:
    print(next_url)
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
            next_url =  base_url + new_url
        else:
            break
    else:
        break
print(links)

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
        author_bio = quote.find("a")["href"]
        all_quotes.append([text.get_text(), author.get_text(), author_bio])


print(f"{len(all_quotes)} quotes scraped")


#encapsulate in a while loop so we can restart if needed
while True:
    #tracks users attempts
    attempts = 4

    #picks a random number for list of quotes
    choice = randint(0, len(all_quotes))

    #picks a random quote from list with choice number 
    question = all_quotes[choice]

    print("Lets play guess the quote! type quit any time to exit the game!")
    print("-" * 20)
    print(question[0]) 
    print(f"Attempts:{attempts}")
    print("Who said this quote?")

    while attempts > 0:
        #get hint information
        hint = requests.get(base_url + question[2])
        soup = BeautifulSoup(hint.text, "html.parser")
        #aquire born date in a list
        born = soup.select(".author-born-date")
        #access list data 
        born_date = born[0].get_text()
        #author location
        location = soup.select(".author-born-location")
        location = location[0].get_text()
        #get user answer
        answer = input()

        #option to quit
        if answer == "quit":
            break

        #attempt 1 logic with first hint
        elif answer != question[1] and attempts == 4:
            attempts -=1
            print("That is incorrect, try again, heres a hint.")
            print(f"The author was born on {born_date} {location}")
            print(f"Attempts:{attempts}")

        #attempt two logic with second hint
        elif answer != question[1] and attempts == 3:
            attempts -=1
            print("That is incorrect, try again, heres another hint.")
            intials = question[1].split(' ')
            print(f"The author's intials are {intials[0][0]}.{intials[1][0]}")
            print(f"Attempts:{attempts}") 

        #attempt three logic with third hint
        elif answer != question[1] and attempts == 2:
            attempts -=1
            print("That is incorrect, last try, heres your final hint.")
            name = question[1].split(' ')
            print(f"The author's first name is {len(name[0])} characters long. ")
            print(f"Attempts:{attempts}") 

        #if answer is correct break second while loop
        elif answer == question[1]:
            print("Thats correct!")
            break
        else:
            print(f"Sorry you loose. The answer was {question[1]}.")
            break
    
    #within the first while loop ask to play again if no break else start again.
    print("Do you want to play again? Y/N")
    play_again = input().lower()
    if play_again == "n":
        print("Thanks for playing! Bye.")
        break
