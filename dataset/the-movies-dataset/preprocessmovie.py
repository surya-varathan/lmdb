import csv
with open('movies_metadata.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    w = [] # output list: a list of tuples
    for i, row in enumerate(csv_reader):
        r = []
        if i == 0:
            targets_cols = ['title', 'id', 'original_language', 'runtime', 'release_date', 'revenue', 'poster_path', 'overview']
            targets = []
            for c in targets_cols:
                targets.append(row.index(c))
        else:
            try:
                for j, t in enumerate(targets):
                    # turn runtime into int
                    if j == 3:
                        r.append(int(float(row[t])))
                    else:
                        r.append(row[t])
            except:
                pass
        if len(r)==len(targets_cols):
            w.append(tuple(r))
            
# check uniqueness
print(len(w))
keys = set()
for row in w:
    if row[1] not in keys:
        keys.add(row[1])
    else:
        w.remove(row)
print(len(w))
# output csv
print('start writing file') 
with open('table_movie.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(targets_cols)
    for i, row in enumerate(w):
        csv_out.writerow(row)
print('finish writing file') 