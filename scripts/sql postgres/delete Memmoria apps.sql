--select count(*) from task where app_id in (select id from app where short_name like '%MemmoriaParaiba1841A1847_tt2%')

delete from task where app_id in (select id from app where short_name like '%MemmoriaParaiba1841A1847%');
delete from app where short_name like '%MemmoriaParaiba1841A1847%';