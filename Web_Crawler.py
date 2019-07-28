#codding is available for SQL attacK and use try...execpt to catch error or to return error.Please see your bro code of webscraping and my code.
# Imports from python libraries
from bs4 import BeautifulSoup
import requests
import MySQLdb as mdb
import time
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Make matplotlib plot the charts in line
get_ipython().magic(u'matplotlib inline')


# In[19]:


# Retrive the HTML code from the page and display the code
# Use the Amazon Editor's Picks of 2017 page's url
url = "https://www.amazon.com/b/ref=s9_acss_bw_cg_BOTY17_1b1_w?node=17296221011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-5&pf_rd_r=DKFR3TF5G550Q0MB0ABB&pf_rd_t=101&pf_rd_p=9df3d953-04ca-4dff-a72a-346eabd56bad&pf_rd_i=17276804011"

# Get data from URL
page = requests.get(url)

# CHECKPOINT: Display HTML page
print (page.text)


# In[20]:


# Parse the HTML in the `page` variable, and store it in BeautifulSoup format
bs = BeautifulSoup(page.text, 'html.parser')

# CHECKPOINT: Check if the parsed HTML content is being stored in the BeautifulSoup format
bs


# In[21]:


# Find all the tags 'li' with class name 'a-carousel-card acswidget-carousel__card'
# All the information about the books is stored between these tags
books = bs.findAll('li','a-carousel-card acswidget-carousel__card')

# Print how many books have been found
print ("Found {} books on the web page\n".format(len(books)))

# CHECKPOINT: Check whether the content between the tags prints for the first book
book_1 = books[0]
book_1


# In[22]:


# For every book object in books retrieve the title, number of reviews, price, and binding type
# The find method uses the tag name and then the class name to identify the tag
# Content returns the content between the tags
# We will print all the information for all the books to ensure that there information is being correctly gathered
for book in books:
    title = book.find('span', 'a-size-base').contents[0]
    reviews = book.find('span','acs_product-rating__review-count').contents[0]
    price = book.find('span','a-size-base a-color-price acs_product-price__buying').contents[0].strip()
    binding = book.find('div','a-row a-color-secondary a-size-small acs_product-metadata__binding').contents[0].strip()
    print (title, reviews, price, binding)


# In[ ]:


# This code creates a connection to the database
con = mdb.connect(host = 'localhost',
                  user = 'root',
                  passwd = 'dwdstudent2015',
                  charset='utf8', use_unicode=True);


# In[ ]:


# Run a query to create a database that will hold the data
# We have named the database "amazon_books"
db_name = 'amazon_books'
create_db_query = "CREATE DATABASE IF NOT EXISTS {db} DEFAULT CHARACTER SET 'utf8'".format(db=db_name)

# Create a database
cursor = con.cursor()
cursor.execute(create_db_query)
cursor.close()


# In[ ]:


# Create the table for storing title, reviews, price and binding of the book
# Primary key has been set as reviews, title
# Table name has been set as "best_of_2017"
cursor = con.cursor()
table_name = 'best_of_2017'
create_table_query = '''CREATE TABLE IF NOT EXISTS {db}.{table}
                                (title varchar(250),
                                 reviews int,
                                 price varchar(250),
                                 binding varchar(250),
                                 PRIMARY KEY(reviews, title)
                                )'''.format(db=db_name, table=table_name)
cursor.execute(create_table_query)
cursor.close()


# In[ ]:


# The information retrieved from the Amazon page needs to be loaded into the databse
# For each book object the code commits the title, reviews, price and binding to the table
query_template = '''INSERT IGNORE INTO {db}.{table}(title,
                                                    reviews,
                                                    price,
                                                    binding)
                    VALUES (%s, %s, %s, %s)'''.format(db=db_name, table=table_name)
cursor = con.cursor()


for book in books:
    title = book.find('span', 'a-size-base').contents[0]
    reviews = book.find('span','acs_product-rating__review-count').contents[0]
    price = book.find('span','a-size-base a-color-price acs_product-price__buying').contents[0].strip()
    binding = book.find('div','a-row a-color-secondary a-size-small acs_product-metadata__binding').contents[0].strip()
    time.sleep(2)
    query_parameters = (title, reviews, price, binding)
    cursor.execute(query_template, query_parameters)

con.commit()
cursor.close()


# A screenshot of the database with the information about title, reviews, price and binding

# ![Screen%20Shot%202017-11-19%20at%208.01.11%20PM.png](attachment:Screen%20Shot%202017-11-19%20at%208.01.11%20PM.png)

# PART 2: This segment of the code retrieves the information from the table created in part 1 and loads it into a pandas dataframe. It then creates two graphs: (1) Plots number of reviews as a function of price (2) Plots a bar graph to see the count of hard cover to paperback books

# In[ ]:


# Set the style of graphs to display large fonts and figures
matplotlib.style.use(['seaborn-talk', 'seaborn-ticks', 'seaborn-whitegrid'])
plt.rcParams['figure.figsize'] = (15, 5)


# In[ ]:


#Establish a connection to the amazon_books database to retrive the information
conn_string_amazon = 'mysql://{user}:{password}@{host}:{port}/{db}'.format(
    user='root',
    password='dwdstudent2015',
    host = 'localhost',
    port=3306,
    db='amazon_books'
)
engine_amazon = create_engine(conn_string_amazon)


# In[ ]:


# First load all the information from the table into a dataframe
# to check if the information is being correctly loaded

# Design a query to retrieve all the information from the best_of_2017 table
# Order by the information by title of the books
query = '''
SELECT*
FROM best_of_2017
ORDER BY title
'''


# In[ ]:


#Query the table and load the information retrieved into pandas dataframe
df_books = pd.read_sql(query, con=engine_amazon)

#CHECKPOINT: Check whether the information is present in the dataframe
df_books


# PLOT 1: This graph will display the number of reviews as a function of price.
#         So price will be on the x axis and number of reviews will be on the y axis.
#         The information will be displayed as a line graph.

# In[ ]:


# Now query the database to retrieve information about reviews and price
# We will use that information to plot a line graph
# Design a query to retrieve the information
query = '''
SELECT reviews, price
FROM best_of_2017
ORDER BY price
'''
# Query the database and display the results
df_book_reviews = pd.read_sql(query, con=engine_amazon)

# CHECKPOINT: Display information about price and reviews only
df_book_reviews.head(5)


# In[ ]:


# Set the x axis as the price variable
# Set the title of the graph to be "Number of Reviews by Price"
# Plot the graph
df_book_reviews = df_book_reviews.set_index('price')
df_book_reviews.plot(title ="Number of Reviews by Price")


# PLOT 2: This graph will display the number of hardcover books and paperback books as a bar graph. The x axis will display the type of binding, and the y axis will have the count.

# In[ ]:


# Design a query to retrieve information about the binding
# Group the books by binding
# Then get a count of the number of books for each type of binding
query = '''
SELECT binding, COUNT(*) AS num_books
FROM best_of_2017
GROUP BY binding
'''
#Query the database for the binding
df_book_reviews3 = pd.read_sql(query, con=engine_amazon)

#CHECKPOINT: Display the information retrieved to check if its accurate
df_book_reviews3


# In[ ]:


# Set the x axis to type of binding
# The y axis will display the count
# Then plot a bar graph using the information retrieved by the query above
df_book_reviews3 = df_book_reviews3.set_index('binding')
df_book_reviews3.plot(kind ="bar")

