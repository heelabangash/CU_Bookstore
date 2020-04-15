import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput, Button, DataTable, DateFormatter, TableColumn, Paragraph, Div
from bokeh.plotting import figure
import bokeh.plotting as plt
import random
import pandas as pd

import sqlalchemy
from sqlalchemy import create_engine
db_string = "postgres://postgres:1234123@localhost:5432/bookstore"
db = create_engine(db_string)

from datetime import date
from random import randint

from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn

sfdf = pd.read_sql('SELECT * FROM storefront LIMIT 10',db).fillna(0)

data = {}

cellheight = 15

for c in sfdf.columns:
    data[c] =  list(sfdf[c])

source = ColumnDataSource(sfdf)

columns = []
for c in sfdf.columns:
    columns.append(TableColumn(field = c, title = c))
cities = pd.read_csv('cities.csv')
    
quantityinputs = [Paragraph(text = 'Enter Quantities for Order', height = 13)]
for x in range(10):
    quantityinputs.append(TextInput(height = cellheight, width = 100))

search_table = DataTable(source=source, columns=columns, width=400, height=280)
def search():
    global search_table
    global sfdf
    global note
    params = {}
    params['title'] = search_params[1].value
    params['authors'] = search_params[2].value
    params['isbn'] = search_params[3].value
    params['genere'] = search_params[4].value
    print(params)
    query = 'SELECT * FROM storefront'
    b = True
    for k in params.keys():
        if(params[k] != ''):
            if b:
                query = query + ' WHERE'
                b = False
            else:
                
                query = query + ' AND'
            query = query + f""" {k} LIKE '%%{params[k]}%%'"""
        
    
    query = query + ' LIMIT 10'
    print(query)
    sfdf = pd.read_sql(query,db).fillna(0)
    print(sfdf)
    search_table.source.data = ColumnDataSource(sfdf).data
    note.text = note.text + '</br>SEARCHING </br></br>SQL:  ' + query.replace('%%', '%')
    print('searching')
    




total = 0
total = '${:,.2f}'.format(total)
cartdata = {}

for c in sfdf.columns:
    cartdata[c] =  []

cartsource = ColumnDataSource(cartdata)

cartcolumns = []
for c in sfdf.columns:
    cartcolumns.append(TableColumn(field = c, title = c))

    
quantityinputs = [Paragraph(text = 'Enter Quantities for Order', height = cellheight)]
for x in range(10):
    quantityinputs.append(TextInput(height = cellheight, width = 100))
    
cart_table = DataTable(source=cartsource, columns=cartcolumns, width=400)


btsearch = Button(label='SEARCH', width = 100, button_type='success')
btsearch.on_click(search)

sw = 92

search_params =[
    Paragraph(text = 'SEARCH', height = cellheight),
    TextInput(title = 'Title:', width  = sw),
    TextInput(title = 'Author:', width = sw),
    TextInput(title = 'ISBN:', width   = sw),
    TextInput(title = 'Genere:', width = sw),
    column(Paragraph(height = 8), btsearch)
    
]

cart = pd.DataFrame(columns = sfdf.columns)
tx_total = Paragraph(text = f'Total = {total}')
def add_to_cart():
    global qauantityinputs
    global sfdf
    global cart
    global cartsource
    global cart_table
    global tx_total
    global total
    global note
    global search_table
    values = []
    idx = 0
    addls = []
    sfdf = sfdf.reset_index(drop = True)
    search_table.source.data = ColumnDataSource(sfdf).data
    for x in quantityinputs[1:-1]:
        print(x)
        print(type(x))
        print(x.value)
        values.append(x.value)
        if((x.value != '') & (idx < len(sfdf))):
            tdf = pd.DataFrame(sfdf.iloc[idx]).T
            if((list(tdf['quantity'])[0] > 0) & (int(x.value) <=  list(tdf['quantity'])[0])):
                if(list(tdf['isbn'])[0] in list(cart['isbn'])):
                    iv = cart[cart['isbn'] == list(tdf['isbn'])[0]].index.values[0]
                    cart.at[iv, 'quantity'] = cart.at[iv, 'quantity'] + int(x.value)
                    print(cart.at[iv,'quantity'])
                    print(iv)
                    if(cart.iloc[iv]['quantity'] < 1):
                        cart = cart.drop([iv], axis = 0)
                        cart = cart.reset_index(drop = True)

                else:
                    if(int(x.value) > 0):
                        tdf['quantity'] = int(x.value)
                        if len(cart) == 0:
                            cart = tdf.copy()
                            cart = cart.reset_index(drop = True)
                        else:
                            cart = pd.concat([cart.copy(),tdf.copy()])
                            cart = cart.reset_index(drop = True)
        x.value = ''
        idx += 1
        
    cartdata = {}
    print(cart)
    for c in cart.columns:
        cartdata[c] =  list(cart[c])

    cartsource = ColumnDataSource(cartdata)
    cart_table.source.data = cartsource.data
    total = sum(cart['price']*cart['quantity'])
    total = '${:,.2f}'.format(total)
    tx_total.text = f'Total = {total}'
    note.text = 'CART CHANGED </br>'

    
def create_user(Email, firstname, lastname, billingaddress, shippingaddress):
    global db
    insert_user = f'''
    INSERT INTO users (Email, firstname, lastname, billingaddress, shippingaddress)
    VALUES ('{Email}', '{firstname}', '{lastname}', '{billingaddress}', '{shippingaddress}')
    '''
    try:
        res = db.execute(insert_user)
        print(res)
    except Exception as e:
        print(e)    
    

def place_order():
    global note
    global billing
    global email
    global shipping
    global cart
    global db
    global uname
    global cart_table
    billingaddress = billing.value
    shippingaddress = shipping.value
    Email = email.value 
    firstname = uname.value.split()[0]
    lastname = uname.value.split()[1]
    note.text = ''
    
    insert_user = f'''
    INSERT INTO users (Email, firstname, lastname, billingaddress, shippingaddress)
    VALUES ('{Email}', '{firstname}', '{lastname}', '{billingaddress}', '{shippingaddress}')
    '''
    try:
        res = db.execute(insert_user)
        note.text = '</br>ADDED AS USER '
    except Exception as e:
        print(e)
    
    tl = []
    
    ISBNs = list(cart['isbn'])
    quantities = [int(x) for x in list(cart['quantity'])]
    order_num = None
    orderlocation = cities.iloc[random.randint(0,len(cities))]['city']
    if len(ISBNs) > 0:
        insert_order = f'''
        INSERT INTO orders (order_num, Email, orderbilling, ordershipping, orderdate, orderlocation)
        VALUES (DEFAULT, '{Email}', '{billingaddress}', '{shippingaddress}', CURRENT_DATE, '{orderlocation}')
        RETURNING order_num
        '''
        try:
            res = db.execute(insert_order)
            print(res)
            tl = list(res)
        except Exception as e:
            print(e)
            
        
        if len(tl) > 0:
            order_num = tl[0][0]
            for i in range(len(ISBNs)):

                isbn = ISBNs[i]
                quantity = quantities[i]
                insert_order_item = f'''
                INSERT INTO orderitems (order_num, isbn, quantity)
                VALUES ({order_num}, '{isbn}', {quantity})
                '''
                try:
                    res = db.execute(insert_order_item)
                    print(res)
                except Exception as e:
                    print(e)
                    
                    
            for i in range(len(ISBNs)):
                isbn = ISBNs[i]
                quantity = quantities[i]
                update_quantities = f'''
                UPDATE books
                SET quantity = quantity - {quantity}
                WHERE isbn = '{isbn}'
                RETURNING quantity
                '''
                try:
                    res = db.execute(update_quantities)
                    remaining = list(res)[0][0]
                    if(remaining < 10):
                        tempdf = pd.read_sql(f"""SELECT sold FROM sales_by_book_30day WHERE isbn = '{isbn}'""", db)                        
                        quantity = int(list(tempdf['sold'])[0])
                        print(f'quantity = {quantity}')
                        note.text = note.text + '</br> ORDERING ' + str(quantity) + ' MORE ISBN: ' + isbn
                        update_book = f'''
                        UPDATE books
                        SET quantity = quantity + {quantity}
                        WHERE isbn = '{isbn}'
                        '''

                        db.execute(update_book)
                    print(res)
                    
                except Exception as e:
                    print(e)
        
        note.text = note.text+'</br>ORDER PLACED </br>ORDER #: ' + str(order_num)
        sfdf = pd.read_sql('SELECT * FROM storefront LIMIT 10',db).fillna(0)
        search_table.source.data = ColumnDataSource(sfdf).data
    #     cart = cart.drop(cart.index, inplace = True)
        cart = pd.DataFrame(columns=cart.columns)
        cart_table.source.data = ColumnDataSource(cart).data

        print('order placed')
    else:
        note.text = 'ORDER FAILED'
    search()

def login():
    global billing
    global email
    global shipping
    global uname
    global note
    global db
    df = None
    
    user_info = f'''
    SELECT * FROM users WHERE email = '{email.value}'
    '''
    try:
        df = pd.read_sql(user_info, db)
    except Exception as e:
        print(e)
    billing.value = list(df['billingaddress'])[0]
    shipping.value = list(df['shippingaddress'])[0]
    uname.value = list(df['firstname'])[0] + '  ' + list(df['lastname'])[0]
    note.text = 'LOGGED IN'
    print('logged in')
    
def register():
    global note
    global billing
    global email
    global shipping
    global cart
    global db
    global uname
    
    billingaddress = billing.value
    shippingaddress = shipping.value
    Email = email.value 
    firstname = uname.value.split()[0]
    lastname = uname.value.split()[1]
    note.text = ''
    
    insert_user = f'''
    INSERT INTO users (Email, firstname, lastname, billingaddress, shippingaddress)
    VALUES ('{Email}', '{firstname}', '{lastname}', '{billingaddress}', '{shippingaddress}')
    '''
    try:
        res = db.execute(insert_user)
        note.text = '</br>REGISTERED'
    except Exception as e:
        note.text = '</br>REGISTRATION FAILED'
        print(e)

def track_order():
    global TX_location
    global TB_order
    global note
    try:
        ordernum = int(TB_order.value)
        location = list(pd.read_sql(f'SELECT orderlocation FROM orders WHERE order_num = {ordernum}',db)
                        .fillna(0)['orderlocation'])[0]
        note.text = 'LOCATION : ' + location
    except:
        note.text = 'ENTER VALID TRACKING #'
    
    
    
bt = Button(label='ADD TO CART', width = 100, button_type='success')
bt.on_click(add_to_cart)

btreg = Button(label='REGISTER', width = 100, button_type='success')
btreg.on_click(register)

bttrac = Button(label='TRACK ORDER', width = 100, button_type='success')
bttrac.on_click(track_order)

TX_location = Paragraph(text = '')
TB_order = TextInput(title = 'Enter Order #:', width  = sw)

btlogin = Button(label='LOGIN', width = 100, button_type='success')
btlogin.on_click(login)

order_button = Button(label='PLACE ORDER', width = 100, button_type='warning')
order_button.on_click(place_order)
email = TextInput(title = 'Enter Email:', width  = sw)
billing = TextInput(title = 'Billing Address:', width  = sw)
shipping = TextInput(title = 'Shipping Address:', width = sw)
uname = TextInput(title = 'Enter Name', width = sw)

note = Div(text = '''
README: 
</br>Use the search to search for books. Partial string will work.
</br>The search will only show the first 10 results.
</br>
</br>Do not sort the table by columns as it will not match the quantity boxes (issue related to bokeh).
</br>
</br>Enter a negative number if you want to remove books from your cart
</br>
</br>Enter your email and "login" to load your address and view past order numers
</br>
</br>Feel free to change these as you check out to have your new order sent/billed to a different address
</br>
</br>If you are not a registered user you will be registered on checkout
''')




quantityinputs.append(bt)
cart_title = Paragraph(text = f'CART')


curdoc().add_root(column(
    column(search_params[0],row(search_params[1:])),row(search_table,column(quantityinputs)), 
    column(cart_title ,
           row(cart_table,
               column(tx_total,row(email,column(Paragraph(height=8),btlogin)), row(uname,column(Paragraph(height=8),btreg)),
                      shipping, 
                      billing,  
                      order_button
                     )
              ),
          ),
    row(TB_order, column(Paragraph(height=8),bttrac), column(Paragraph(height=8),TX_location)),
    note,
    width=1600))
curdoc().title = "Select Books To Order"
