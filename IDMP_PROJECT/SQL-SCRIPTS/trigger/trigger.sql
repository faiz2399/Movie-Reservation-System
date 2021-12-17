delimiter $$
create trigger confirmation 
after insert on booking 
for each row
begin
		insert into confirmation(user_id,confirmed)
		values(new.user_id,'Confirmed');
END$$
DELIMITER ;