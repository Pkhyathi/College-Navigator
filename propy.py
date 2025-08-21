from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# Function to load college data from MySQL database
def load_college_data():
    college_data = []
    try:
        # Connect to MySQL database using pymysql
        connection = pymysql.connect(
            host="127.0.0.1",  # MySQL server host (localhost or IP)
            user="root",  # MySQL username
            password="pkhyathi28",  # MySQL password
            database="mini5"  # Your MySQL database
        )

        if connection.open:
            cursor = connection.cursor()

            # Query to fetch all college data from the 'kcet' table
            cursor.execute("SELECT college_name, branch, cutoff_rank, category FROM kcet")
            rows = cursor.fetchall()

            # Process each row
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
        # Close the connection
        if connection.open:
            cursor.close()
            connection.close()

    return college_data

# Function to find colleges based on rank and category (case insensitive)
def clg_rank_direct(rank, category, cd):
    av_clg = []
    category = category.strip().upper()  # Convert the input category to uppercase

    for clg_data in cd:
        clg = clg_data['college_name']
        br = clg_data['branch']
        co = clg_data['cutoff_rank']
        cat = clg_data['category'].strip().upper()  # Convert database category to uppercase

        # Check eligibility based on rank and category (case-insensitive)
        if rank <= co and category == cat:
            av_clg.append((clg, br))
    
    return av_clg

@app.route("/", methods=["GET", "POST"])
def index():
    eligible_colleges = []
    if request.method == "POST":
        try:
            # Get user input for rank and category
            rank = int(request.form["rank"])
            category = request.form["category"].strip()

            # Load college data from MySQL database
            college_data = load_college_data()

            # Find eligible colleges for the entered category
            eligible_colleges = clg_rank_direct(rank, category, college_data)

        except ValueError:
            eligible_colleges = []

    return render_template("prohtml.html", eligible_colleges=eligible_colleges)

if __name__ == "__main__":
    app.run(debug=True)
