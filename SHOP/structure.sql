create database SHOP;
use SHOP;
create table users(uid int(5) PRIMARY KEY AUTO_INCREMENT, uname varchar(20), passwd varchar(20));
create table items(iid int(5) PRIMARY KEY AUTO_INCREMENT, itm_name varchar(20), itm_price float(10,2), itm_qty int(10));
