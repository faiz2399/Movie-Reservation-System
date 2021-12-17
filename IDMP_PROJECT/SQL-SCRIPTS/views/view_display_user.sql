create view display_user as 
select u.username, b.movie_id , m.movie_name
from booking as b, users as u,movie as m
where b.user_id = u.id and b.movie_id = m.movie_id ;