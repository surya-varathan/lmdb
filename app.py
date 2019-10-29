from flask import Flask, render_template, request ,redirect , session , flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

import psycopg2

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

try:
    conn = psycopg2.connect("dbname=lmdb user=fevenz")
    cur = conn.cursor()
except:
    print("Can't connect to database")


@app.route("/")
def index():
    return render_template('search.html')

@app.route("/movie/<movieid>" , methods=['GET','POST'])
def movie(movieid):
    if request.method == "GET":
        cmd = "SELECT * FROM movie where mov_id={0}".format(movieid)
        cur.execute(cmd)
        movie = cur.fetchone()
        if movie == None:
            return render_template("error.html" , message = "Enter valid Movie Id")
        cmd = "SELECT director_id FROM direct where mov_id={0}".format(movieid)
        cur.execute(cmd)
        director_id = cur.fetchone()[0]
        cmd = "SELECT name FROM director where director_id={0}".format(director_id)
        cur.execute(cmd)
        director_name = cur.fetchone()[0]
        director_tuple = (director_name,director_id)
        cmd = "SELECT * FROM act where mov_id={0}".format(movieid)
        cur.execute(cmd)
        casts = cur.fetchall()
        cast_list = list()
        for cast in casts:
            role = cast[1]
            cmd = "SELECT name,cast_id FROM mov_cast where cast_id={0}".format(cast[2])
            cur.execute(cmd)
            name , cast_id = cur.fetchone()
            cast_list.append((name,cast_id,role))
        cur.execute("SELECT username, comment, rating from rating WHERE mov_id = {0}".format(movieid))                           
        reviews = cur.fetchall()
        return render_template("movie.html" , movie_details = movie , cast_list = cast_list , director = director_tuple , reviews = reviews)
    else:

        currentUser = session["username"]
        
        rating = request.form.get("rating")
        comment = request.form.get("comment")
        
        cur.execute("SELECT * FROM rating WHERE username = '{0}' AND mov_id = {1}".format
                    (currentUser,movieid) )
        row2 = cur.fetchone() 

        if row2:
            flash('You already submitted a review for this movie', 'warning')
            return redirect("/movie/" + movieid)

        rating = int(rating)

        cur.execute("INSERT INTO rating (mov_id, username,rating , comment) VALUES ({0}, '{1}', {2}, '{3}')".format(movieid,currentUser,rating,comment))
        
        conn.commit()

        flash('Review submitted!', 'info')

        return redirect("/movie/" + movieid)


@app.route("/director/<directorid>")
def director(directorid):
    cmd = "SELECT * FROM director where director_id={0}".format(directorid)
    cur.execute(cmd)
    result = cur.fetchone()
    cmd = "SELECT mov_id FROM direct where director_id={0}".format(directorid)
    cur.execute(cmd)
    movies = cur.fetchall()
    movie_list = []
    for movie in movies:
        movieid = movie[0]
        cmd = "SELECT * FROM movie where mov_id={0}".format(movieid)
        cur.execute(cmd)
        movie_item = cur.fetchone()
        movie_list.append(movie_item)
    return render_template("director.html" , director_details = result , movie_list = movie_list)


@app.route("/cast/<castid>")
def actor(castid):
    cmd = "SELECT * FROM mov_cast where cast_id={0}".format(castid)
    cur.execute(cmd)
    result = cur.fetchone()
    print(result)
    cmd = "SELECT mov_id FROM act where cast_id={0}".format(castid)
    cur.execute(cmd)
    movies = cur.fetchall()
    movie_list = []
    for movie in movies:
        movieid = movie[0]
        cmd = "SELECT * FROM movie where mov_id={0}".format(movieid)
        cur.execute(cmd)
        movie_item = cur.fetchone()
        movie_list.append(movie_item)
    return render_template("cast.html" , cast_details = result , movie_list = movie_list)


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register user """
    
    session.clear()
    
    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("error.html", message="must provide username")

        username = request.form.get("username")
        cmd = "SELECT * FROM users where username='{0}'".format(username)
        cur.execute(cmd)
        userCheck = cur.fetchone()

        if userCheck:
            return render_template("error.html", message="username already exist")

        elif not request.form.get("password"):
            return render_template("error.html", message="must provide password")

        elif not request.form.get("confirmation"):
            return render_template("error.html", message="must confirm password")

        elif not request.form.get("password") == request.form.get("confirmation"):
            return render_template("error.html", message="passwords didn't match")
        
        hashedPassword = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        
        cmd = "INSERT INTO users (username, hash) VALUES ('{0}', '{1}')".format(username,hashedPassword)
        cur.execute(cmd)
        conn.commit()


        return redirect("/login")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log user in """

    session.clear()

    username = request.form.get("username")

    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("error.html", message="must provide username")

        elif not request.form.get("password"):
            return render_template("error.html", message="must provide password")

        username = request.form.get("username")
        cmd = "SELECT * FROM users where username='{0}'".format(username)
        cur.execute(cmd)
        result = cur.fetchone()

        if result == None or not check_password_hash(result[1], request.form.get("password")):
            return render_template("error.html", message="invalid username and/or password")

        session["username"] = result[0]
        session["hash"] = result[1]

        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """ Log user out """

    session.clear()

    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
def search():
    if not request.args.get("movie"):
        return render_template("error.html", message="you must provide a movie.")

    query = "%" + request.args.get("movie") + "%"

    query = query.title()
    
    cur.execute("SELECT * from movie WHERE \
                        name LIKE '{0}'  \
                        LIMIT 15".format(query))

    rows = cur.fetchall()
    
    # movies not founded
    if not rows:
        return render_template("error.html", message="we can't find movies with that description.")
    
    # Fetch all the results
    movies = rows

    return render_template("results.html", movies = movies)


if __name__ == "__main__":
    
    app.debug = True
    app.run()