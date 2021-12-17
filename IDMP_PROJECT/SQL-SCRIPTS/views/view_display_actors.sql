create view display_actors as 
select m.movie_name , a.name
from actor_in_movie as am , movie as m , actor as a
where am.movie_id = m.movie_id and a.actor_id = am.actor_id
