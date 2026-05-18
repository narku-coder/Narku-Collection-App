from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_connection

app = Flask(__name__)
app.secret_key = "narku_collect"

@app.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT COUNT(*) AS c FROM booktable")
    book_count = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) AS c FROM cdtable")
    cd_count = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) AS c FROM boardgames")
    board_game_count = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) AS c FROM videogames")
    video_game_count = cur.fetchone()["c"]


    cur.close()
    conn.close()
    return render_template(
        "index.html",
        books_count=book_count,
        cds_count=cd_count,
        board_games_count=board_game_count,
        video_games_count=video_game_count,
    )

# ---------- BOOKS ----------

@app.route("/books")
def books_list():
    q = request.args.get("q", "").strip()
    field = request.args.get("field", "title")
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    if q:
        cur.execute(
            "SELECT * FROM booktable WHERE title LIKE %s OR author LIKE %s",
            (f"%{q}%", f"%{q}%")
        )
    else:
        cur.execute("SELECT * FROM booktable")
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("books_list.html", books=books, q=q, field=field)

@app.route("/books/add", methods=["GET", "POST"])
def books_add():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        year_published = request.form.get("year_published")
        publisher = request.form.get("publisher")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO booktable (title, author, year_published, publisher) VALUES (%s, %s, %s, %s)",
            (title, author, year_published, publisher)
        )
        cur.close()
        conn.close()
        flash("Book added successfully.")
        return redirect(url_for("books_list"))
    return render_template("books_add.html")

# ---------- CDS ----------

@app.route("/cds")
def cds_list():
    q = request.args.get("q", "").strip()
    field = request.args.get("field", "title")
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    if q:
        cur.execute(
            "SELECT * FROM cdtable WHERE title LIKE %s OR artist LIKE %s",
            (f"%{q}%", f"%{q}%")
        )
    else:
        cur.execute("SELECT * FROM cdtable")
    cds = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("cds_list.html", cds=cds, q=q, field=field)

@app.route("/cds/add", methods=["GET", "POST"])
def cds_add():
    if request.method == "POST":
        title = request.form.get("title")
        artist = request.form.get("artist")
        year_released = request.form.get("year_released")
        label = request.form.get("label")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO cdtable (title, artist, year_released, label) VALUES (%s, %s, %s, %s)",
            (title, artist, year_released, label)
        )
        cur.close()
        conn.close()
        flash("Cd added successfully.")
        return redirect(url_for("cds_list"))
    return render_template("cds_add.html")

# ---------- BOARD GAMES ----------

@app.route("/boardGames")
def board_games_list():
    q = request.args.get("q", "").strip()
    field = request.args.get("field", "title")
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    if q:
        cur.execute(
            "SELECT * FROM boardgames WHERE title LIKE %s OR company LIKE %s",
            (f"%{q}%", f"%{q}%")
        )
    else:
        cur.execute("SELECT * FROM boardgames")
    board_games = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("board_games_list.html", board_games=board_games, q=q, field=field)

@app.route("/boardGames/add", methods=["GET", "POST"])
def board_games_add():
    if request.method == "POST":
        title = request.form.get("title")
        company = request.form.get("company")
        year_released = request.form.get("year_released")
        category = request.form.get("category")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO boardgames (title, company, year_released, category) VALUES (%s, %s, %s. %s)",
            (title, company, year_released, category)
        )
        cur.close()
        conn.close()
        flash("Board Game added successfully.")
        return redirect(url_for("board_games_list"))
    return render_template("board_games_add.html")

# ---------- VIDEO GAMES ----------

@app.route("/videoGames")
def video_games_list():
    q = request.args.get("q", "").strip()
    field = request.args.get("field", "title")
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    if q:
        cur.execute(
            "SELECT * FROM videogames WHERE title LIKE %s OR developer LIKE %s",
            (f"%{q}%", f"%{q}%")
        )
    else:
        cur.execute("SELECT * FROM videogames")
    video_games = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("video_games_list.html", video_games=video_games, q=q, field=field)

@app.route("/videoGames/add", methods=["GET", "POST"])
def video_games_add():
    if request.method == "POST":
        title = request.form.get("title")
        developer = request.form.get("developer")
        year_released = request.form.get("year_released")
        genre = request.form.get("genre")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO videogames (title, developer, year_released, genre) VALUES (%s, %s, %s. %s)",
            (title, developer, year_released, genre)
        )
        cur.close()
        conn.close()
        flash("Video Game added successfully.")
        return redirect(url_for("video_games_list"))
    return render_template("video_games_add.html")

@app.route("/search")
def global_search():
    q = request.args.get("q", "").strip()
    scope = request.args.get("scope", "all")

    books = []
    cds = []
    board_games = []
    video_games = []

    if not q:
        # If empty query, just show an empty results page
        return render_template(
            "search_results.html",
            q=q,
            scope=scope,
            books=books,
            cds=cds,
            board_games=board_games,
            video_games=video_games
        )

    conn = get_connection()
    cur = conn.cursor(dictionary=True, buffered=True)

    # Search books only or as part of "all"
    if scope in ("all", "books"):
        cur.execute(
            "SELECT book_id, title, author FROM booktable WHERE title LIKE %s OR author LIKE %s",
            (f"%{q}%", f"%{q}%")
        )
        books = cur.fetchall()

    # Search cds only or as part of "all"
    if scope in ("all", "cds"):
        cur.execute(
            """
            SELECT cd_id, title, artist
            FROM cdtable
            WHERE title LIKE %s OR artist LIKE %s
            """,
            (f"%{q}%", f"%{q}%")
        )
        cds = cur.fetchall()

    # Search board games only or as part of "all"
    if scope in ("all", "board_games"):
        cur.execute(
            "SELECT board_game_id, title, company FROM boardgames WHERE title LIKE %s OR company LIKE %s",
            (f"%{q}%", f"%{q}%")
        )
        board_games = cur.fetchall()

    # Search video games only or as part of "all"
    if scope in ("all", "video_games"):
        cur.execute(
            "SELECT game_id, title, developer FROM videogames WHERE title LIKE %s OR developer LIKE %s",
            (f"%{q}%", f"%{q}%") 
        )
        video_games = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "search_results.html",
        q=q,
        scope=scope,
        books=books,
        cds=cds,
        board_games=board_games,
        video_games=video_games
    )
if __name__ == "__main__":
    app.run(debug=True)
