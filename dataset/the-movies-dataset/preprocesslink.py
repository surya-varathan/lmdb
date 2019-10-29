import csv
import ast

with open('./table_movie.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    m = []
    for i, row in enumerate(csv_reader):
        m.append(row[1])
    m = set(m)
    
# link 
with open('movies_metadata.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    w = [] # output list: a list of tuples
    for i, row in enumerate(csv_reader):
        r = []
        if i == 0:
            targets_cols = ['id', 'imdb_id']
            targets = []
            for c in targets_cols:
                targets.append(row.index(c))
        else:
            for j, t in enumerate(targets):
                if row[targets[0]] in m:
                    if j == 0:
                        r.append(row[t])
                    if j ==1 and row[t] != '' and row[t].startswith('tt'):
                        r.append(row[t])
        if len(r)==len(targets_cols):
            w.append(tuple(r))
            
# check uniqueness
print(len(w))
w = set(w)
print(len(w))
# output csv
print('start writing file') 
with open('table_link.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['mov_id', 'web_id'])
    for i, row in enumerate(w):
        csv_out.writerow(row)
print('finish writing file') 