/*
 * script para criacao das tabelas do banco
 * de dados do Memoria Estatistica do Brasil
 */

drop table book cascade;
drop table page cascade;
drop table workflow_transaction cascade;
drop table page_table cascade;
drop table metadata cascade;
drop table cell cascade;
drop table report cascade;

create table book(
	id varchar(255) primary key,
	
	title varchar(255),
	publisher varchar(255),
	contributor varchar(255),
	volume varchar(50),
	img_url varchar(255),
	initialDate date,
	finalDate date
);

create table page(
	id int,
	local_url varchar(255),
	archive_url varchar(255),
	
	book_id varchar(255),
	
	foreign key (book_id) references book(id),
	constraint page_pk primary key (id, book_id)
);

create table workflow_transaction(
	id serial primary key,
	
	app_id int,
	t1_id int,
	t2_id int,
	t3_id int,
	t4_id int 
);

create table page_table(
	id serial,
	
	page_id int,
	book_id varchar(255),
	
	initialDate date,
	finalDate date,
	
	local_url varchar(255),
	
	top_pos int check(top_pos >= 0),
	left_pos int check(left_pos >= 0),
	down_pos int check(down_pos >= 0),
	right_pos int check(right_pos >= 0),
	
	constraint fk_page_id foreign key (page_id, book_id) references page(id, book_id),
	constraint pk_table primary key (id, page_id, book_id)
);

create table metadata (
	id serial,
	
	page_table_id int,
	page_id int,
	book_id varchar(255),
	
	source varchar(255),
	footer varchar(255),
	title varchar(255),
	subtitle varchar(255),
	subject varchar(255),
	
	constraint pk_metadata primary key (id, page_table_id, page_id, book_id),
	constraint fk_page_table foreign key (page_table_id, page_id, book_id) references page_table(id, page_id, book_id)
);

create table cell(
	id serial primary key,
	
	page_table_id int,
	page_id int,
	book_id varchar(255),
	
	x0 int check(x0 >= 0),
	y0 int check(y0 >= 0),
	x1 int check(x1 >= 0),
	y1 int check(y1 >= 0),
	
	text varchar(255),
	
	constraint fk_cell foreign key(page_table_id, page_id, book_id) references page_table(id, page_id, book_id)
);

create table report(
	id serial primary key,
	
	task_id int,
	app_id int,
	
	message varchar(255)
);
