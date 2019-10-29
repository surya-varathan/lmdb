import csv

with open('movies_metadata.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    w = [] # output list: a list of tuples
    for i, row in enumerate(csv_reader):
        r = []
        if i == 0:
            targets_cols = ['imdb_id']
            targets = []
            for c in targets_cols:
                targets.append(row.index(c))
        else:
            for j, t in enumerate(targets):
                if row[t] != '':
                    r.append(row[t])
            w.append(tuple(r))
            
# check uniqueness
print(len(w))
w = set(w)
print(len(w))
# output csv
print('start writing file') 
with open('table_website.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['web_id'])
    for i, row in enumerate(w):
        csv_out.writerow(row)
print('finish writing file') 