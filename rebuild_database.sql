drop database if exists panda;
create database panda default char set 'utf8';
update account_user_profile set role=0 where user_id in (select id from auth_user where username='manager');