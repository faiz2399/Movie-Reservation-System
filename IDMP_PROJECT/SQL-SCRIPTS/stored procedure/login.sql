delimiter $$
create procedure login_proc(in email_1 varchar(64) , in username_1 varchar(64), in pasword_hash_1 varchar(128))
begin 
	insert into users(email, username, password)
    values(email_1, username_1, pasword_hash_1);
            
end$$

delimiter ;