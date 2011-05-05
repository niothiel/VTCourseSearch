DROP TABLE VTCS.Courses;

CREATE TABLE VTCS.Courses (
	id integer primary key auto_increment,
	email text not null,
	crn integer not null,
	term text not null,
	created timestamp default NOW(),
	done boolean default False
);

INSERT INTO VTCS.Courses (email, crn, term) VALUES ("asdf@asdf.com", 6969, "FALL 2011");
