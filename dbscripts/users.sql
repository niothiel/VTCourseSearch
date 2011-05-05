DROP TABLE VTCS.Users;

CREATE TABLE VTCS.Users (
	id integer primary key auto_increment,
	email text not null,
	pass text not null
);

INSERT INTO VTCS.Users (email, pass) VALUES ("asdf@asdf.com", "password");
