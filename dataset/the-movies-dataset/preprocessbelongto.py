import csv
import ast

with open('./table_movie.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    m = []
    for i, row in enumerate(csv_reader):
        m.append(row[1])
    m = set(m)

with open('movies_metadata.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    w = []
    for i, row in enumerate(csv_reader):
        r = []
        if i == 0:
            movie_index = row.index('id')
            genres_index = row.index('genres')
            targets = [movie_index, genres_index]
            header_length = len(row)
        else:
            if len(row) == header_length:
                for i, t in enumerate(targets):
                    genre_ids = []
                    if i ==1:
                        dicts = ast.literal_eval(row[t])
                        for d in dicts:
                            genre_ids.append(d['id'])
                    else:
                        movie_id = row[t]
                for g in genre_ids:
                    if movie_id in m:
                        r.append((movie_id, g))
                for p in r:
                    w.append(tuple(p))
                    
print(len(w))
w = set(w)
print(len(w))
with open('table_belong_to.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['mov_id', 'genre_id'])
    for i, row in enumerate(w):
        csv_out.writerow(row)