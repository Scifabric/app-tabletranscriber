select info from task_run where app_id in (select id from app where short_name like '%anuario1916pb%')

--delete from task where app_id in (select id from app where short_name like '%anuario1916pb%')
--delete from app where short_name like '%anuario1916pb%'


select count(*) from task where app_id in (select id from app where short_name like '%anuario1916pb%') 