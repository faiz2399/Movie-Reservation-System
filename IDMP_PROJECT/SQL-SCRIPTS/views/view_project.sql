create view display_schedule as 
select s.schedule_id, movie_name, s.date,s.time
from schedule as s, movie as m
where m.movie_id = s.movie_id and m.movie_status = 'A';
            