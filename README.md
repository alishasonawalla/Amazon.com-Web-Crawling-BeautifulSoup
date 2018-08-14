# Web-Crawling-Beautiful-Soup

This code performs two tasks:

1. First, the code crawls Amazon.com's page on Best Books of 2017 (Editor's Picks) to retrieve information. The code uses BeautifulSoup to crawl and then collects the title of the book, number of reviews, price of the book and type of binding (hardcover/paperback). The information retrieved from Amazon.com is then loaded into a database called amazon_books and into a table called best_of_2017.

2. Then, the code queries the best_of_2017 table to load the information into a pandas dataframe. The dataframe is information is used to make 2 plots - a line graph showing the correlation between price and number of reviews and a bar plot to show the number of books by binding type.


