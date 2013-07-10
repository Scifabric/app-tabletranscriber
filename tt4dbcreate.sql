create table book(

id varchar(255) primary key,
title varchar(255),
publisher varchar(255),
contributor varchar(255)

);

create table page(

id int,
url varchar(255),
book_id varchar(255),
foreign key(book_id) references book(id),
constraint page_pk primary key(id, book_id)

);

create table page_table(

id int not null,
url varchar(255),
top_pos int,
left_pos int,
page_id int not null,
book_id varchar(255) not null,
source varchar(255),
footer varchar(255),
title varchar(255),
subtitle varchar(255),
context varchar(255),
constraint fk_page_table foreign key(page_id, book_id) references page(id, book_id),
constraint pk_table primary key(id, page_id, book_id)

);

create table cell(

id serial primary key,
table_id int,
book_id varchar(255),
page_id int,
x0 int,
y0 int,
x1 int,
y1 int,
text varchar(255),
foreign key(table_id, page_id, book_id) references page_table(id, page_id, book_id)

);
