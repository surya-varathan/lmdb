import psycopg2

commands = (
        """
        DROP TABLE IF EXISTS website CASCADE;
        CREATE TABLE website( 
        web_id VARCHAR(255),
        PRIMARY KEY (web_id)
        );
        """,
        """
        DROP TABLE IF EXISTS act CASCADE;
        CREATE TABLE act(
        mov_id int,
        role text,
        cast_id int,
        PRIMARY KEY (mov_id, cast_id),
        FOREIGN KEY (mov_id) REFERENCES movie (mov_id),
        FOREIGN KEY (cast_id) REFERENCES mov_cast (cast_id)
        );
        """
    )



conn = psycopg2.connect("dbname=lmdb user=fevenz")
cur = conn.cursor()
for command in commands:
    cur.execute(command)

conn.commit()
    

