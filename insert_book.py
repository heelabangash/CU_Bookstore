import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput, Button, Div
from bokeh.plotting import figure
import bokeh.plotting as plt
from bokeh.palettes import Spectral6
from bokeh.plotting import figure


import pandas as pd

import sqlalchemy
from sqlalchemy import create_engine
db_string = "postgres://postgres:1234123@localhost:5432/bookstore"
db = create_engine(db_string)

#

note = Div(text = 'README: Only ISBN and Quantity are required to update Quantity')

def insert_book(
    isbn, 
    title, 
    genere, 
    publishername, 
    numpages, 
    price, 
    percentage,
    quantity,
    authors, 
    address, 
    email, 
    phonenumber, 
    bankaccount
):
    global db
    if(note.text != 'UPDATING INVENTORY'):
        insert_book = f'''
        INSERT INTO books (isbn, title, genere, publishername, numpages, price, percentage, quantity)
        VALUES ('{isbn}', '{title}', '{genere}', '{publishername}', {numpages}, {price}, {percentage}, {quantity})
        '''
        try:
            db.execute(insert_book)
        except Exception as e:
            e = str(e).split(' duplicate')[0]
            print(e)
            if(e == '(psycopg2.errors.UniqueViolation)'):
                print(e)
    else:
        update_book = f'''
        UPDATE books
        SET quantity = {quantity}
        WHERE isbn = '{isbn}'
        '''

        db.execute(update_book)
    if(note.text != 'UPDATING INVENTORY'):    
        for author in authors:
            firstname = author[0]
            lastname = author[1]
            insert_author = f'''
            INSERT INTO Authors (isbn, firstname, lastname)
            VALUES ('{isbn}', '{firstname}', '{lastname}')
            '''
            try:
                db.execute(insert_author)
            except Exception as e:
                print(e)

        insert_publisher = f'''
        INSERT INTO publishers (publishername, address, email, phonenumber, bankaccount)
        VALUES ('{publishername}', '{address}', '{email}', '{phonenumber}', '{bankaccount}')
        '''
        try:
            db.execute(insert_publisher)
        except Exception as e:
            print(e)



TEXT_ISBN = TextInput(title="ISBN:")
TEXT_title = TextInput(title="Title:")
TEXT_authors = TextInput(title="Author(s): (use comma for multiple authors)")
TEXT_genere = TextInput(title="Genere:")
TEXT_numpages = TextInput(title="# Pages:")
TEXT_publishername = TextInput(title="Publisher Name:")
TEXT_publishaddress = TextInput(title="Publisher Address:")
TEXT_publishemail = TextInput(title="Publisher Email:")
TEXT_publishphone = TextInput(title="Publisher Phone#:")
TEXT_bankaccount = TextInput(title="Publisher Bank Account:")
TEXT_percentage = TextInput(title="Publisher %:")
TEXT_quantity = TextInput(title="Quantity:")
TEXT_price = TextInput(title="Price (CAD):")




def insert_book_handler():
    isbn = 0
    title = 0
    authors = 0
    genere = 0
    numpages = 0
    publishername = 0
    address = 0
    email = 0
    phonenumber = 0
    bankaccount = 0
    percentage = 0
    price =  0
    quantity = 0
    authors = []
    try:
        isbn = TEXT_ISBN.value
        quantity = int(TEXT_quantity.value)
        title = TEXT_title.value
        authors = TEXT_authors.value
        genere = TEXT_genere.value
        numpages = int(TEXT_numpages.value)
        publishername = TEXT_publishername.value
        address = TEXT_publishaddress.value
        email = TEXT_publishemail.value
        phonenumber = TEXT_publishphone.value
        bankaccount = TEXT_bankaccount.value
        percentage = float(TEXT_percentage.value)
        price =  float(TEXT_price.value)
        ta = authors.split(',')
        
        for author in ta:
            print(author)
            authors.append(author.split())
    except:
        if((isbn) != 0 & (quantity != 0)):
            note.text = 'UPDATING INVENTORY'
    
    
    insert_book(
    isbn, 
    title, 
    genere, 
    publishername, 
    numpages, 
    price, 
    percentage,
    quantity,
    authors, 
    address, 
    email, 
    phonenumber, 
    bankaccount
    )

bt = Button(label='Insert Book')
bt.on_click(insert_book_handler)




# output_file("colormapped_bars.html")

fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
counts = [5, 3, 4, 2, 4, 6]

from bokeh.plotting import figure, output_file
from bokeh.io import show
from bokeh.models import ColumnDataSource, ranges
from bokeh.plotting import figure
import pandas as pd


dat = pd.DataFrame([['A',20],['B',20],['C',30]], columns=['category','amount'])

source = ColumnDataSource(dict(x=[],y=[]))

x_label = "Category"
y_label = "Amount"
title = "BAR PLOT"
import itertools
from bokeh.models.ranges import FactorRange
import math
plot = figure(plot_width=600, plot_height=600,
        x_axis_label = x_label,
        y_axis_label = y_label,
        title=title,
             x_range=FactorRange(factors=list(dat.category)) 
        )
source = ColumnDataSource(dict(x=[],y=[], color=[]))
plot.vbar(source=source,x='x',top='y',color = 'color', bottom=0,width=0.3)
plot.xaxis.major_label_orientation = math.pi/2



def authorview():
    global plot
    global db
    global source
    tempdf = pd.read_sql('SELECT * FROM sales_by_author', db)
    colors = colors = itertools.cycle(Spectral6)
    c = []
    for i, x in enumerate(colors):
        c.append(x)
        print(i)
        if(i == len(tempdf)-1):
            break
    source.data = dict(
        x = tempdf.author,
        y = tempdf.sold,
        color = c
    )
    plot.x_range.factors = list(source.data['x'])

BTauthors = Button(label='Author View', width = 100)
BTauthors.on_click(authorview)

def bookview():
    global plot
    global db
    global source
    tempdf = pd.read_sql('SELECT * FROM sales_by_book', db)
    colors = colors = itertools.cycle(Spectral6)
    c = []
    for i, x in enumerate(colors):
        c.append(x)
        print(i)
        if(i == len(tempdf)-1):
            break
    source.data = dict(
        x = tempdf.isbn,
        y = tempdf.sold,
        color = c
    )
    plot.x_range.factors = list(source.data['x'])

BTbooks = Button(label='Book View', width = 100)
BTbooks.on_click(bookview)

def genereview():
    global plot
    global db
    global source
    tempdf = pd.read_sql('SELECT * FROM sales_by_genere', db)
    colors = itertools.cycle(Spectral6)
    c = []
    for i, x in enumerate(colors):
        c.append(x)
        print(i)
        if(i == len(tempdf)-1):
            break
    source.data = dict(
        x = tempdf.genere,
        y = tempdf.sold,
        color = c
    )
    plot.x_range.factors = list(source.data['x'])

BTgenere = Button(label='Genere View', width = 100)
BTgenere.on_click(genereview)

def grossview():
    global plot
    global db
    global source
    global note
#     note.text = str(pd.read_sql('SELECT * FROM sales_by_book', db))
    tempdf = pd.read_sql('SELECT * FROM sales_by_book', db)
    colors = colors = itertools.cycle(Spectral6)
    c = []
    for i, x in enumerate(colors):
        c.append(x)
        print(i)
        if(i == len(tempdf)-1):
            break
    source.data = dict(
        x = tempdf.publishername,
        y = tempdf.grossincome,
        color = c
    )
    plot.x_range.factors = list(source.data['x'])

BTgross = Button(label='Gross', width = 100)
BTgross.on_click(grossview)

def publisherview():
    global plot
    global db
    global source
    global note
#     note.text = str(pd.read_sql('SELECT * FROM sales_by_book', db))
    tempdf = pd.read_sql('SELECT * FROM sales_by_book', db)
    colors = colors = itertools.cycle(Spectral6)
    c = []
    for i, x in enumerate(colors):
        c.append(x)
        print(i)
        if(i == len(tempdf)-1):
            break
    source.data = dict(
        x = tempdf.publishername,
        y = tempdf.publishershare,
        color = c
    )
    plot.x_range.factors = list(source.data['x'])

BTpub = Button(label='Expenditures', width = 100)
BTpub.on_click(publisherview)

inputs = column(TEXT_ISBN,
                TEXT_title,
                TEXT_authors,
                TEXT_genere,
                TEXT_numpages,
                TEXT_publishername,
                TEXT_publishaddress,
                TEXT_publishemail,
                TEXT_publishphone,
                TEXT_bankaccount,
                TEXT_percentage,
                TEXT_price,
                TEXT_quantity,
                bt,
                note
               )

curdoc().add_root(row(inputs, column(plot, row(BTauthors, BTbooks, BTgenere, BTgross, BTpub)) ,width=800))
curdoc().title = "ADD/REMOVE/UPDATE BOOKS"
