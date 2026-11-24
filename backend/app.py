from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)

CORS(app)

DATABASE = "library.db"

def connect_db():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn

def create_table():

    conn = connect_db()

    conn.execute("""

    CREATE TABLE IF NOT EXISTS books(

        studentId TEXT PRIMARY KEY,

        studentName TEXT,

        bookName TEXT,

        status TEXT

    )

    """)

    conn.commit()

    conn.close()

create_table()

@app.route('/api/books', methods=['GET'])
def get_books():

    search = request.args.get("search", "")

    conn = connect_db()

    rows = conn.execute(
        "SELECT * FROM books WHERE studentName LIKE ?",
        ('%' + search + '%',)
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])

@app.route('/api/books', methods=['POST'])
def add_book():

    data = request.json

    studentId = data.get("studentId")
    studentName = data.get("studentName")
    bookName = data.get("bookName")

    if not studentId or not studentName or not bookName:
        return jsonify({"error":"All fields required"}),400

    try:

        conn = connect_db()

        conn.execute(
            "INSERT INTO books VALUES (?,?,?,?)",
            (studentId, studentName, bookName, "Issued")
        )

        conn.commit()

        conn.close()

        return jsonify({"message":"Book Issued"}),201

    except:
        return jsonify({"error":"Student already exists"}),400

@app.route('/api/books/return/<studentId>', methods=['PUT'])
def return_book(studentId):

    conn = connect_db()

    conn.execute(
        "UPDATE books SET status='Returned' WHERE studentId=?",
        (studentId,)
    )

    conn.commit()

    conn.close()

    return jsonify({"message":"Returned"})

@app.route('/api/books/<studentId>', methods=['DELETE'])
def delete_book(studentId):

    conn = connect_db()

    conn.execute(
        "DELETE FROM books WHERE studentId=?",
        (studentId,)
    )

    conn.commit()

    conn.close()

    return jsonify({"message":"Deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
