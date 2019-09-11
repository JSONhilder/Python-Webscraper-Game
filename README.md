# Python Web scraping Game

Using Python, BeautifulSoup and the requests module to scrap the website, http://quotes.toscrape.com/.

Using the scraped data to then create a CLI guessing game where the user has three attempts to guess the author of the quote.

After each guess using the scraped information hints will be given to the player.

## Want to play? 

- Clone the repo

- Install pipenv

        pip install pipenv

- Create the virtual environment

        pipenv shell

- Sync and install the files from pipfile

        pipenv sync

- Make sure you are in the virtual env and run the scraper to scrape files and add contents to a CSV named quotes.csv
        This can be automated or ran every once in a while for an update

        python csv_scraper.py

- Now run the game file

        python game.py