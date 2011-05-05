CREATE TABLE VTCS.Courses (
	id integer primary key auto_increment,
	email text not null,
	crn integer not null,
	term text not null,
	created timestamp default NOW(),
	done boolean default False
);
