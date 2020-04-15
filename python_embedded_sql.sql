/*note the following sql commands are embedded in the python files
they are listed here just for doumentation*/

/* Automatically generated query for search (allows partial matching)

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
*/

/* insert user (note {x} is used in a formatted string to embed variable x out of the python environment)
this is used when a user registers or when a new user places an order (automatically registers new users)

insert_user = f'''
    INSERT INTO users (Email, firstname, lastname, billingaddress, shippingaddress)
    VALUES ('{Email}', '{firstname}', '{lastname}', '{billingaddress}', '{shippingaddress}')
    '''
*/

/* creates an order and returns the order number from the table
insert_order = f'''
        INSERT INTO orders (order_num, Email, orderbilling, ordershipping, orderdate, orderlocation)
        VALUES (DEFAULT, '{Email}', '{billingaddress}', '{shippingaddress}', CURRENT_DATE, '{orderlocation}')
        RETURNING order_num
        '''
*/

/* Creates an order item with a foreign key on the generated order numbers
insert_order_item = f'''
                INSERT INTO orderitems (order_num, isbn, quantity)
                VALUES ({order_num}, '{isbn}', {quantity})
                '''
*/


/* finds the quantity sold in the last 30 days when stock goes below 10 and "orders" 
that many from the publisher by updating the quantity

tempdf = pd.read_sql(f"""SELECT sold FROM sales_by_book_30day WHERE isbn = '{isbn}'""", db)                        
                        quantity = int(list(tempdf['sold'])[0])
                        print(f'quantity = {quantity}')
                        note.text = note.text + '</br> ORDERING ' + str(quantity) + ' MORE ISBN: ' + isbn
                        update_book = f'''
                        UPDATE books
                        SET quantity = quantity + {quantity}
                        WHERE isbn = '{isbn}'
                        '''
*/


/* default serch for the storfront
SELECT * FROM storefront LIMIT 10
*/


/* gets the location of an order number
SELECT orderlocation FROM orders WHERE order_num = {ordernum}
*/

/* when a user enters their email and clicks "login" this query will return their defualt addresses
SELECT * FROM users WHERE email = '{email.value}'
*/


/* inserts a new book into the books table
insert_book = f'''
        INSERT INTO books (isbn, title, genere, publishername, numpages, price, percentage, quantity)
        VALUES ('{isbn}', '{title}', '{genere}', '{publishername}', {numpages}, {price}, {percentage}, {quantity})
*/

/* allows owners to update stock manually 
UPDATE books
        SET quantity = {quantity}
        WHERE isbn = '{isbn}'
*/

/* attempts to add a publisher to the publisher table (will fail if already exists)
INSERT INTO publishers (publishername, address, email, phonenumber, bankaccount)
        VALUES ('{publishername}', '{address}', '{email}', '{phonenumber}', '{bankaccount}')
		*/
		
/* selects from views to show performance/sales/costs and update plots
SELECT * FROM sales_by_author
SELECT * FROM sales_by_book
SELECT * FROM sales_by_genere
SELECT * FROM sales_by_book
SELECT * FROM sales_by_book_30day
*/