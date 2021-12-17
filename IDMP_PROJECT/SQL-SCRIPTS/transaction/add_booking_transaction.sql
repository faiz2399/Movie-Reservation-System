delimiter $$
create procedure add_booking_transaction(in s_id int , in u_name varchar(64) )
begin
	declare exit handler for sqlexception rollback;
    
	insert into booking(schedule_id,movie_id,user_id)
	select S.schedule_id, movie_id, U.id
	from schedule S natural left outer join users U
	where S.schedule_id = s_id and U.username = u_name;
    
	start transaction;
    
    update schedule
    set seats = seats-1
    where schedule_id = s_id;
    
    commit;
end $$
delimiter ;