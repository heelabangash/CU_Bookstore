To run this webapp these are the following requirements
Python 3.7 environment with bokeh and sqlalchemy psycopg2
a postgresql database named bookstore
psql in your system path 
change the login in the .py files to match your database

psql -U postgres -d bookstore -a -f build_tables.sql
*replace postgres with your username if it is different

go to your directory with the python files and run the folowing

bokeh serve create_order.py

open another command prompt (or detatch and create a new screen)

bokeh serve insert_book.py --port 5007

opern your browser to 

http://localhost:5007/insert_book

http://localhost:5006/create_order

Have fun!