delimiter $$
create procedure BOOKING(in user_name varchar(64))
begin

    select username,booking_id,movie_id,schedule_id
	from booking B join users U
	on B.user_id = U.id 
	where U.username = user_name;
end$$
delimiter ;