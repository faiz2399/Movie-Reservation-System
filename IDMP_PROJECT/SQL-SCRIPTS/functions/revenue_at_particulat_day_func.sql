delimiter $$
create function revenue_at_particular_day(sch_date date)
returns int
deterministic
begin
declare rev int;

select sum(100 - seats) into rev
from schedule natural join movie
where movie_status = 'A' and date = sch_date;

return rev*50;
end $$
delimiter ; 