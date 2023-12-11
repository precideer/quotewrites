# Quotewrites

Quotewrites is a Flask application designed to allow users to practice creative writing by responding to literary book quote prompts. Through the website, users can create a personal account, browse through hundreds of thought-provoking quotes from (mostly Western) literary canon, save the quotes that speak to them, and work on writing exercises in response to their chosen prompts.

_**Acknowledgement:** Quotes in the database were extracted from Litquotes.com._

## Markdown/programming languages

HTML, CSS, JavaScript, Python, SQLite3

## Setup and configuration

- Upload the zipped folder to an appropriate environment (e.g. VSCode w/ WSL), unzip the folder / extract all files and folders within.
- The relevant dependencies can be installed by running `pip install -r requirements.txt`.
- To view the database, run `sqlite3 quotewrites.db` in the terminal.
- To run `app.py`, run `python3 app.py` in the terminal.
- To open the application in a local browser, run `flask run` in the terminal and click on the link provided.

## File overview

- `quotewrites.db` is an SQLite3 database that stores all quotes, users, and the users' quotewrites
- `app.py` is the main Python source code for the website
- `helpers.py` has helper functions (apology, login_required)
- `static/styles.css` contains the CSS styling for the website
- `templates` is a folder containing all of the website's HTML pages
	- `apology.html`: error message
	- `index.html`: website homepage
	- `layout.hmtl`; template from which other files are extended
	- `login.html`: user log-in page
	- `register.html`: user registration page
	- `my_quotewrites.html`: dashboard of bookmarked/written Quotewrites
	- `prompt.html`: displays new randomly chosen literary book quotes from the database
	- `write.html`: where users can create and edit their Quotewrites
- `get_quotes` is a folder containing files (in folder `quotes`) of HTML code from Litquotes.com, where quotes were extracted using the `get_quotes.py` program. This was originally where/how `quotewrites.db` was created, and does not need to be used to run the finished Quotewrites application

## YouTube introduction

https://youtu.be/dfynsKFNiBo
