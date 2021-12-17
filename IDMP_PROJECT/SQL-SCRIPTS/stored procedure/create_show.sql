delimiter $$
create procedure create_show( in movie_id int, in date date, in time time)
begin
	insert into schedule(movie_id,date,time)
    values(movie_id,date,time);
end $$
delimiter ;