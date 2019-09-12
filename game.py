import requests
from bs4 import BeautifulSoup
from random import randint
from csv import reader

BASE_URL = "http://quotes.toscrape.com"

def  read_quotes(filename):
    with open(filename, "r", encoding="utf-8") as file:
        csv_reader = reader(file)
        return list(csv_reader)

def play_game(quotes):
    attempts = 4

    choice = randint(1, len(quotes))

    question = quotes[choice]

    print("Lets play guess the quote! type quit any time to exit the game!")
    print("-" * 20)
    print(question[0]) 
    print(f"Attempts:{attempts}")
    print("Who said this quote?")

    while attempts > 0:
        hint = requests.get(BASE_URL + question[2])
        soup = BeautifulSoup(hint.text, "html.parser")
        born = soup.select(".author-born-date")
        born_date = born[0].get_text()
        location = soup.select(".author-born-location")
        location = location[0].get_text()
        answer = input()

        if answer == "quit":
            break

        elif answer != question[1] and attempts == 4:
            attempts -=1
            print("That is incorrect, try again, heres a hint.")
            print(f"The author was born on {born_date} {location}")
            print(f"Attempts:{attempts}")

        elif answer != question[1] and attempts == 3:
            attempts -=1
            print("That is incorrect, try again, heres another hint.")
            intials = question[1].split(' ')
            print(f"The author's intials are {intials[0][0]}.{intials[1][0]}")
            print(f"Attempts:{attempts}") 

        elif answer != question[1] and attempts == 2:
            attempts -=1
            print("That is incorrect, last try, heres your final hint.")
            name = question[1].split(' ')
            print(f"The author's first name is {len(name[0])} characters long. ")
            print(f"Attempts:{attempts}") 

        elif answer == question[1]:
            print("Thats correct!")
            break
        else:
            print(f"Sorry you loose. The answer was {question[1]}.")
            break

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