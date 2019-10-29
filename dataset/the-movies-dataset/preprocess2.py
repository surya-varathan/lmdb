import psycopg2

def insert_csv(file_path, table_name):
    """ insert csv into tables in the PostgreSQL database"""
    conn = None
    try:
        # read the connection parameters
        # connect to the PostgreSQL server
        conn = psycopg2.connect("dbname=lmdb user=fevenz")
        cur = conn.cursor()
        # insert csv files
        f = open(file_path, "r")
        # Truncate the table first
        cur.execute("Truncate {} Cascade;".format(table_name))
        print("Truncated {}".format(table_name))
        # Load table from the file with header
        cur.copy_expert("copy {} from STDIN CSV HEADER QUOTE '\"'".format(table_name), f)
        print("Loaded data into {}".format(table_name))
        # close communication with the PostgreSQL database server
        cur.close()
        f.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

#insert_csv('table_movie.csv', 'movie')
#insert_csv('table_genre.csv', 'genre')
#insert_csv('table_director.csv', 'director')
#insert_csv('table_direct.csv', 'direct')
#insert_csv('table_mov_cast.csv', 'mov_cast')
insert_csv('table_act.csv', 'act')
#insert_csv('table_belong_to.csv', 'belong_to')
#insert_csv('table_website.csv', 'website')
#insert_csv('table_link.csv', 'link')