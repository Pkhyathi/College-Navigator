import webbrowser
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pymysql
import os

app = Flask(__name__)

IMAGE_FOLDER = r"C:\Users\Khyathi Paruchuri\OneDrive\Desktop\Mini Project 5"

def load_college_data():
    college_data = []
    try:
        connection = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="pkhyathi28",
            database="mini5"
        )
        if connection.open:
            cursor = connection.cursor()
            cursor.execute("SELECT college_name, branch, cutoff_rank, category FROM kcet")
            rows = cursor.fetchall()
            for row in rows:
                college_data.append({
                    'college_name': row[0],
                    'branch': row[1],
                    'cutoff_rank': row[2],
                    'category': row[3]
                })
    except pymysql.MySQLError as e:
        print(f"Error loading data from MySQL: {e}")
    finally:
        if connection.open:
            cursor.close()
            connection.close()
    return college_data

def clg_rank_direct(rank, category, cd):
    av_clg = []
    category = category.strip().upper()
    for clg_data in cd:
        clg = clg_data['college_name']
        br = clg_data['branch']
        co = clg_data['cutoff_rank']
        cat = clg_data['category'].strip().upper()
        if rank <= co and category == cat:
            av_clg.append((clg, br))
    return av_clg

@app.route("/", methods=["GET", "POST"])
def index():
    eligible_colleges = []
    if request.method == "POST":
        try:
            rank = int(request.form["rank"])
            category = request.form["category"].strip()
            college_data = load_college_data()
            eligible_colleges = clg_rank_direct(rank, category, college_data)
            return redirect(url_for("results", rank=rank, category=category))
        except ValueError:
            eligible_colleges = []
    return render_template("prohtml.html", eligible_colleges=eligible_colleges)

@app.route("/results")
def results():
    rank = int(request.args.get("rank"))
    category = request.args.get("category")
    college_data = load_college_data()
    eligible_colleges = clg_rank_direct(rank, category, college_data)
    return render_template("pror.html", eligible_colleges=eligible_colleges, rank=rank, category=category)

@app.route("/get_image/<filename>")
def get_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)   