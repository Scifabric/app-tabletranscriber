CREATE OR REPLACE FUNCTION pseudo_encrypt(VALUE int) returns bigint AS $$
DECLARE
	l1 int;
	l2 int;
	r1 int;
	r2 int;
	i int:=0;
BEGIN
	 l1:= (VALUE >> 16) & 65535;
	 r1:= VALUE & 65535;
	 WHILE i < 3 LOOP
	   l2 := r1;
	   r2 := l1 # ((((1366.0 * r1 + 150889) % 714025) / 714025.0) * 32767)::int;
	   l1 := l2;
	   r1 := r2;
	   i := i + 1;
 END LOOP;
 RETURN ((l1::bigint << 16) + r1);
END;
$$ LANGUAGE plpgsql strict immutable;

create table facts(
	id serial primary key,
	user_id varchar(255),
	book_id varchar(255),
	page_id int not null,
	top_pos int not null,
	left_pos int not null,
	bottom_pos int not null,
	right_pos int not null,
	post_id varchar(255),
	fact_text varchar(255)
);

ALTER TABLE facts ALTER COLUMN id SET DEFAULT pseudo_encrypt(nextval('facts_id_seq')::int);
