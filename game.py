import requests
from bs4 import BeautifulSoup
from random import randint
from csv import reader

#home url for scraping
BASE_URL = "http://quotes.toscrape.com"

def  read_quotes(filename):
    with open(filename, "r", encoding="utf-8") as file:
        csv_reader = reader(file)
        return list(csv_reader)

#create a function and give it a yes no question at the end if the answer is yes return the function again to create a loop
def play_game(quotes):
    #tracks users attempts
    attempts = 4

    #picks a random number for list of quotes
    choice = randint(1, len(quotes))

    #picks a random quote from list with choice number 
    question = quotes[choice]

    print("Lets play guess the quote! type quit any time to exit the game!")
    print("-" * 20)
    print(question[0]) 
    print(f"Attempts:{attempts}")
    print("Who said this quote?")

    while attempts > 0:
        #get hint information
        hint = requests.get(BASE_URL + question[2])
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
    if play_again == "y":
        return play_game(quotes)
    elif play_again == "n":
        print("Thanks for playing! Bye.")
    else:
        print("Please enter either Y or N.")
        play_again = input().lower()

quotes = read_quotes("quotes.csv")
play_game(quotes)