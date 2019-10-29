import csv
import ast
with open('movies_metadata.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    w = []
    for i, row in enumerate(csv_reader):
        if i == 0:
            targets = [row.index('genres')]
        else:
            for i, t in enumerate(targets):
                dicts = ast.literal_eval(row[t])
                for d in dicts:
                    w.append((d['name'], d['id']))
print(len(w))
w = set(w)
print(len(w))
print(w)
with open('table_genre.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['name', 'genre_id'])
    for i, row in enumerate(w):
        csv_out.writerow(row)