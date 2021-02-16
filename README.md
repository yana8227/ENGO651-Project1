# Project 1 (video published at https://youtu.be/QR04g-ol9dU)

ENGO 551

This is a book review web application. Its main functions containing registration, login, searching books by ISBN, author name, or book title (supports partial searching), get detailed info and past reviews of books, and writing reviews for books.


application.py -- orgonizes the functions of the main page, login page, registation page, search page, and book page. 

import.py -- initializes the user_info table, reviews table, and books table, as well as importing book data into the books table.


Inside the templates folder:

layout.html -- setting a base style and structure for all html pages in the templates folder

index.html -- the main page that asks user to login or register

Login.html -- the login page. user need to provide a registered username and password to login

register.html -- the registration page. User need to provide an un-registered username and a password to register. After registration, user will be directed to the login page.

search.html -- After loggging in, user is directed to the main search page where user is able to search for books with the book's ISBN, author name, or book title. Partial search is enabled such that providing an incomplete word will still result in author names or book names that contain the word to be listed. 

book.html -- After clicking on a search result in the search.html page, user will be directed to the book.html page which provides the detailed information of the book, fields to rate and write reviews for the book (a dropdown rating and a text field to leave comments).

error -- Any of the pages above could result in error, the error page is responsible for displaying errors with speficied error messages.
