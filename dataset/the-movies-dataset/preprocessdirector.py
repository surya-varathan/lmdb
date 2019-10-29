import csv
import ast

with open('credits.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    w = []
    for i, row in enumerate(csv_reader):
        if i == 0:
            crew_index = row.index('crew')
            targets = [crew_index]
        else:
            for i, t in enumerate(targets):
                dicts = ast.literal_eval(row[t])
                for d in dicts:
                    if d.get('job') == 'Director':
                        w.append((d.get('name'), d.get('id'), d.get('gender')))
print(len(w))
w = set(w)
print(len(w))
with open('table_director.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['name','director_id', 'gender'])
    for i, row in enumerate(w):
        csv_out.writerow(row)