import csv
import ast

with open('./table_movie.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    m = []
    for i, row in enumerate(csv_reader):
        m.append(row[1])
    m = set(m)

with open('credits.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    w = []
    for i, row in enumerate(csv_reader):
        if i == 0:
            crew_index = row.index('crew')
            movie_index = row.index('id')
            targets = [crew_index]
        else:
            movie_id = row[movie_index]
            for i, t in enumerate(targets):
                dicts = ast.literal_eval(row[t])
                for d in dicts:
                    if d.get('job') == 'Director':
                        director_id = d.get('id')
                        if movie_id in m:
                            w.append((movie_id, director_id))
print(len(w))
w = set(w)
print(len(w))
with open('table_direct.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['mov_id', 'director_id'])
    for i, row in enumerate(w):
        csv_out.writerow(row)