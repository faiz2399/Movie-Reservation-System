delimiter $$
create procedure cancellation(in book_id int, in sched_id int)
begin 
	declare exit handler for sqlexception rollback;
    
    delete from booking
    where booking_id = book_id;
    
    start transaction;
    
    update schedule
    set seats = seats+1
    where schedule_id = sched_id;
    
    commit;
end $$
delimiter ;