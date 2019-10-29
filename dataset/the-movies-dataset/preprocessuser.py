import random
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
import csv
import names

# user_most_like
user_info = dict()
with open('ratings.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for i, row in enumerate(csv_reader):
        r = []
        if i == 0:
            userId = row.index('userId')
            movieId = row.index('movieId')
            rating = row.index('rating')
        else:
            user_info[row[userId]] = user_info.get(row[userId], [])
            user_info[row[userId]].append((row[movieId], row[rating]))
            
# need movie-genre info
movie_genre_info = dict()
with open('./table_belong_to.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for i, row in enumerate(csv_reader):
        if i == 0:
            pass
        else:
            movie_genre_info[row[0]] = row[1]

w = []
# schema: name, user_id, genre_id, gender, birthday,
for k, v in user_info.items():
    # randomly generate male user
    if int(k) % 2 ==0: 
        n = names.get_full_name(gender='female')
    else:
        n = names.get_full_name(gender='male')
    u_id = int(k)
    u_name = k
    passwd = generate_password_hash('password')
    try:
        g_id = int(movie_genre_info[max(user_info['1'], key= lambda x: x[1])])
    except:
        g_id = int(random.choice(list(movie_genre_info.values())))
    g = int(int(k) % 2) 
    year = random.randint(1950, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    b = datetime(year, month, day)
    w.append((n, u_name, passwd, g_id, g, b))

print(len(w))
w = set(w)
print(len(w))
print('start writing file') 
with open('table_user_most_like.csv','w') as out:
    csv_out=csv.writer(out)
    #csv_out.writerow(['name', 'user_id', 'username', 'password', 'genre_id', 'gender', 'birthday'])
    csv_out.writerow(['name', 'username', 'password', 'genre_id', 'gender', 'birthday'])
    for i, row in enumerate(w):
        csv_out.writerow(row)
print('finish writing file')