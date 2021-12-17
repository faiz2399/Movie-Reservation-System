delimiter $$
create procedure delete_status()
begin
	update movie
	set movie_status = null;
end $$
delimiter ;