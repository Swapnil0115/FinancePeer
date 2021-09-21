create table users
(
ID int AUTO_INCREMENT,
Username varchar(255),
Password varchar(255), 
Email varchar(255), 
Full_Name varchar(255),
PRIMARY KEY (ID)
);


create table jsonuser
(
primid int AUTO_INCREMENT,
id int,
userID int,
title varchar(255),
body varchar(255),
userids varchar(255),
PRIMARY KEY (primid)
);