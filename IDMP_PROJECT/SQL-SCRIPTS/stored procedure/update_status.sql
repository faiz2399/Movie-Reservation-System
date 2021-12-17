delimiter $$
create procedure update_status(mov_id int)
begin
	update movie
	set movie_status = 'A'
	where movie_id = mov_id;
end $$
delimiter ;
