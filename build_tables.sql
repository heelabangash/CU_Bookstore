
/*This requires a database called bookstore to run properly
psql -U postgres -d bookstore -a -f build_tables.sql*/

CREATE TABLE IF NOT EXISTS Books (
    ISBN varchar(30),
    Title varchar(120),
    Genere varchar(30),
    PublisherName varchar(60),
    NumPages int,
    Price float,
    Percentage float,
    Quantity int,
    PRIMARY KEY (ISBN)
);

CREATE TABLE IF NOT EXISTS Authors (
    ISBN varchar(30),
    FirstName varchar(30),
    LastName varchar(30),
    PRIMARY KEY (ISBN, FirstName, LastName),
    FOREIGN KEY (ISBN) REFERENCES Books(ISBN)
);

CREATE TABLE IF NOT EXISTS Publishers (
    PublisherName varchar(60),
    Address varchar(120),
    Email varchar(60),
    PhoneNumber varchar(30),
    BankAccount varchar(30),
    PRIMARY KEY (PublisherName)
);

CREATE TABLE IF NOT EXISTS Users (
    Email varchar(60),
    FirstName varchar(30),
    LastName varchar(30),
    BillingAddress varchar(120),
    ShippingAddress varchar(120),
    PRIMARY KEY (Email)
);

DROP TABLE IF EXISTS Orders CASCADE;

CREATE TABLE IF NOT EXISTS Orders (
    Order_num SERIAL,
    Email varchar(60),
    OrderBilling varchar(120),
    OrderShipping varchar(120),
    OrderDate DATE,
    OrderLocation varchar(120),
    PRIMARY KEY (Order_num),
    FOREIGN KEY (Email) REFERENCES Users(Email)
);


DROP TABLE IF EXISTS OrderItems;
CREATE TABLE IF NOT EXISTS OrderItems (
    Order_num int,
    ISBN varchar(30),
    Quantity int,
    PRIMARY KEY (Order_num, ISBN),
    FOREIGN KEY (Order_num) REFERENCES Orders(Order_num)
);

DROP VIEW storefront;

CREATE VIEW storefront AS
SELECT authors.isbn, 
books.title,
books.genere,
books.numpages,
string_agg(concat(authors.firstname, ' ', authors.lastname) , ', ') authors, 
books.price,
books.quantity
FROM authors 
INNER JOIN books
ON authors.isbn = books.isbn
GROUP BY authors.isbn, books.title, books.genere, books.numpages, books.price, books.quantity;



CREATE VIEW sales_by_book AS
SELECT 
books.isbn,
sum(orderitems.quantity) as sold,
sum(orderitems.quantity) * min(books.price) as grossincome,
sum(orderitems.quantity) * min(books.percentage) * min(books.price) as publishershare,
books.price,
books.percentage,
publishers.bankaccount,
publishers.publishername
FROM orderitems
INNER JOIN orders
ON orderitems.order_num =  orders.order_num
INNER JOIN books
ON orderitems.isbn = books.isbn
Inner JOIN publishers
ON books.publishername = publishers.publishername
GROUP BY
books.price,
books.percentage,
publishers.bankaccount,
publishers.publishername,
books.isbn;


CREATE VIEW sales_by_book_30day AS
SELECT 
books.isbn,
sum(orderitems.quantity) as sold,
sum(orderitems.quantity) * min(books.price) as grossincome,
sum(orderitems.quantity) * min(books.percentage) * min(books.price) as publishershare,
books.price,
books.percentage,
publishers.bankaccount,
publishers.publishername
FROM orderitems
INNER JOIN orders
ON orderitems.order_num =  orders.order_num
AND orders.orderdate > current_date - interval '30' day
INNER JOIN books
ON orderitems.isbn = books.isbn
Inner JOIN publishers
ON books.publishername = publishers.publishername
GROUP BY
books.price,
books.percentage,
publishers.bankaccount,
publishers.publishername,
books.isbn;

CREATE VIEW sales_by_genere AS
SELECT 
books.genere,
sum(orderitems.quantity) as sold,
sum(orderitems.quantity * books.price) as grossincome,
sum(orderitems.quantity * books.percentage * books.price) as publishershare
FROM orderitems
INNER JOIN orders
ON orderitems.order_num =  orders.order_num
INNER JOIN books
ON orderitems.isbn = books.isbn
Inner JOIN publishers
ON books.publishername = publishers.publishername
GROUP BY
books.price,
books.percentage,
publishers.bankaccount,
publishers.publishername,
books.isbn;

CREATE VIEW sales_by_author AS
SELECT 
concat(authors.firstname, ' ', authors.lastname) as author,
sum(orderitems.quantity) as sold
FROM orderitems
INNER JOIN orders
ON orderitems.order_num =  orders.order_num
INNER JOIN books
ON orderitems.isbn = books.isbn
INNER JOIN authors
ON authors.isbn = books.isbn
GROUP BY
authors.firstname,
authors.lastname,
books.isbn;
