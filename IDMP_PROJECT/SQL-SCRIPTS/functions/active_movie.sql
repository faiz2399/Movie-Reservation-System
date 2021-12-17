select *
from movieDELIMITER $$
CREATE DEFINER=`root`@`localhost` FUNCTION `active_mov`() RETURNS int(11)
    DETERMINISTIC
begin
declare mov_count int;

select count(*) into mov_count
from movie
where movie_status = 'A';

return mov_count;
end$$
DELIMITER ;
