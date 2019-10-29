import csv
import ast

with open('credits.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    w = []
    for i, row in enumerate(csv_reader):
        if i == 0:
            cast_index = row.index('cast')
            targets = [cast_index]
        else:
            for i, t in enumerate(targets):
                dicts = ast.literal_eval(row[t])
                for d in dicts:
                    w.append((d.get('name'), d.get('id'), d.get('gender')))
print(len(w))
w = list(set(w))
print(len(w))
id_set = set()
for row in w:
    if row[1] not in id_set:
        id_set.add(row[1])
    else:
        w.remove(row)
print(len(w))
with open('table_mov_cast.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['name','cast_id', 'gender'])
    for i, row in enumerate(w):
        csv_out.writerow(row)