import csv
with open('./table_movie.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    m = []
    for i, row in enumerate(csv_reader):
        m.append(row[1])
    m = set(m)
    
with open('ratings.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    w = []
    for i, row in enumerate(csv_reader):
        if row[1] in m:
            w.append((row[1], row[0], int(float(row[2])), ''))

# check uniqueness            
print(len(w))
keys = set()
for row in w:
    if (row[0],row[1]) not in keys:
        keys.add((row[0],row[1]))
    else:
        w.remove(row)
print(len(w))
# output csv
print('start writing file') 
with open('table_rate.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['movieId', 'userId', 'rating'])
    for i, row in enumerate(w):
        csv_out.writerow(row)
print('finish writing file')