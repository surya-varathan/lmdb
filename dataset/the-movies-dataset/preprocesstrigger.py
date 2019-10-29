import psycopg2
cmd = """CREATE trigger before_delete_movie
BEFORE delete on movie
for each row
when (old.mov_id > 0)
BEGIN
	delete from act where mov_id = old.mov_id;
	delete from belong_to where mov_id = old.mov_id;
	delete from rating where mov_id = old.mov_id;
END; """

conn = psycopg2.connect("dbname=lmdb user=fevenz")
cur = conn.cursor()
cur.execute(cmd)
conn.commit()