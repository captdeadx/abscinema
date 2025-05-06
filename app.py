from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort, send_from_directory
import sqlite3
import os
import hashlib
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'insecure_secret_key_for_demo_purposes'  # Deliberately insecure for demo

# Database setup
DB_NAME = "abs_cinema.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Table 1: Cinema Seats
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cinema_seats (
        id INTEGER PRIMARY KEY,
        cinema_name TEXT NOT NULL,
        movie_name TEXT NOT NULL,
        show_time TEXT NOT NULL,
        total_seats INTEGER DEFAULT 500,
        booked_seats INTEGER DEFAULT 0
    )
    ''')

    # Table 2: Bookings
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        cinema_name TEXT NOT NULL,
        movie_name TEXT NOT NULL,
        show_time TEXT NOT NULL,
        attendees INTEGER NOT NULL,
        total_price REAL NOT NULL,
        discount REAL DEFAULT 0,
        final_price REAL NOT NULL,
        booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_admin_booking INTEGER DEFAULT 0
    )
    ''')

    # Table 3: Users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0
    )
    ''')

    # Initialize cinema_seats with default data
    cinemas = ['Sathiyam', 'INOX', 'Luxe', 'PVR']
    movies = ['Thunderbolts', 'Retro', 'Tourist Family', 'Amore']
    show_times = ['12:00 PM', '10:00 PM']

    # Check if cinema_seats is empty
    cursor.execute("SELECT COUNT(*) FROM cinema_seats")
    if cursor.fetchone()[0] == 0:
        # Initialize cinema seats for all combinations
        seat_id = 1
        for cinema in cinemas:
            for movie in movies:
                for show_time in show_times:
                    cursor.execute(
                        "INSERT INTO cinema_seats (id, cinema_name, movie_name, show_time, total_seats, booked_seats) VALUES (?, ?, ?, ?, 500, 0)",
                        (seat_id, cinema, movie, show_time)
                    )
                    seat_id += 1

    # Initialize users if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Add users
        users = [
            (1, 'user1', 'password123', 0),
            (2, 'admin', '@dM!N', 1),
            (3, 'user2', 'Pass22', 0),
            (4, 'user3', 'Pass33', 0),
            (5, 'user4', 'Pass44', 0)
        ]
        cursor.executemany("INSERT INTO users (id, username, password, is_admin) VALUES (?, ?, ?, ?)", users)

    conn.commit()
    conn.close()


# Create user info text file
def create_user_info_file():
    with open('users_info.txt', 'w') as file:
        file.write("CINEMA BOOKING SYSTEM - USER CREDENTIALS\n")
        file.write("=====================================\n\n")
        file.write("Regular Users:\n")
        file.write("1. Username: user1, Password: password123\n")
        file.write("2. Username: user2, Password: Pass22\n")
        file.write("3. Username: user3, Password: Pass33\n")
        file.write("4. Username: user4, Password: Pass44\n\n")
        file.write("Administrator:\n")
        file.write("Username: admin, Password: @dM!N\n\n")
        file.write("Note: This file is accessible via URL, demonstrating path traversal vulnerability.\n")


# Initialize database on startup
init_db()
create_user_info_file()


# Routes
@app.route('/')
def root():
    return redirect(url_for('cinema'))


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/cinema')
def cinema():
    return render_template('cinema.html')


@app.route('/api/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # Deliberately vulnerable to SQL injection
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Vulnerable query - DO NOT USE IN PRODUCTION
        query = f"SELECT id, username, is_admin FROM users WHERE username = '{username}' AND password = '{password}'"

        try:
            cursor.execute(query)
            user = cursor.fetchone()

            if user:
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['is_admin'] = user[2]

                return jsonify({
                    'success': True,
                    'user_id': user[0],
                    'username': user[1],
                    'is_admin': bool(user[2])
                })
            else:
                return jsonify({'success': False, 'message': 'Invalid credentials'})
        except sqlite3.Error as e:
            return jsonify({'success': False, 'message': str(e)})
        finally:
            conn.close()


@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})


@app.route('/api/cinema_data')
def cinema_data():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cinema_seats")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append(dict(row))

    conn.close()
    return jsonify(result)


@app.route('/api/book', methods=['POST'])
def book():
    if request.method == 'POST':
        data = request.json

        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not logged in'})

        # For regular bookings
        if 'cinema' in data:
            cinema = data.get('cinema')
            movie = data.get('movie')
            time = data.get('time')
            attendees = int(data.get('attendees'))
            discount = float(data.get('discount', 0))
            ticket_price = 10  # Fixed price
            total_price = ticket_price * attendees
            final_price = total_price - discount

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            # Generate booking ID
            booking_id = f"BK{datetime.now().strftime('%y%m%d%H%M%S')}"

            # Vulnerable check without transaction - susceptible to race conditions
            cursor.execute(
                "SELECT total_seats, booked_seats FROM cinema_seats WHERE cinema_name = ? AND movie_name = ? AND show_time = ?",
                (cinema, movie, time)
            )
            seat_info = cursor.fetchone()

            if not seat_info:
                conn.close()
                return jsonify({'success': False, 'message': 'Invalid cinema, movie or time'})

            total_seats, booked_seats = seat_info

            if total_seats - booked_seats < attendees and not session.get('is_admin'):
                conn.close()
                return jsonify({'success': False, 'message': 'Not enough seats available'})

            # Update booked seats
            cursor.execute(
                "UPDATE cinema_seats SET booked_seats = booked_seats + ? WHERE cinema_name = ? AND movie_name = ? AND show_time = ?",
                (attendees, cinema, movie, time)
            )

            # Insert booking
            cursor.execute(
                """
                INSERT INTO bookings 
                (booking_id, user_id, cinema_name, movie_name, show_time, attendees, total_price, discount, final_price, is_admin_booking) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (booking_id, session['user_id'], cinema, movie, time, attendees, total_price, discount, final_price, 0)
            )

            conn.commit()
            conn.close()

            return jsonify({
                'success': True,
                'booking_id': booking_id,
                'cinema': cinema,
                'movie': movie,
                'time': time,
                'attendees': attendees,
                'total_price': total_price,
                'discount': discount,
                'final_price': final_price
            })

        # For admin mass bookings
        elif 'admin_bookings' in data:
            admin_bookings = data.get('admin_bookings')

            if not session.get('is_admin'):
                return jsonify({'success': False, 'message': 'Not authorized'})

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            result_bookings = []

            for booking in admin_bookings:
                cinema = booking.get('cinema')
                movie = booking.get('movie')
                time = booking.get('time')
                attendees = int(booking.get('attendees'))
                discount = float(booking.get('discount', 0))
                ticket_price = 10
                total_price = ticket_price * attendees
                final_price = total_price - discount

                # Generate booking ID
                booking_id = f"ADMIN-BK{datetime.now().strftime('%y%m%d%H%M%S')}-{len(result_bookings)}"

                # Insert booking (admin can exceed capacity)
                cursor.execute(
                    """
                    INSERT INTO bookings 
                    (booking_id, user_id, cinema_name, movie_name, show_time, attendees, total_price, discount, final_price, is_admin_booking) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (booking_id, session['user_id'], cinema, movie, time, attendees, total_price, discount, final_price,
                     1)
                )

                result_bookings.append({
                    'booking_id': booking_id,
                    'cinema': cinema,
                    'movie': movie,
                    'time': time,
                    'attendees': attendees,
                    'total_price': total_price,
                    'discount': discount,
                    'final_price': final_price
                })

            conn.commit()
            conn.close()

            return jsonify({
                'success': True,
                'bookings': result_bookings
            })

        return jsonify({'success': False, 'message': 'Invalid request format'})


@app.route('/users_info.txt')
def users_info():
    return send_from_directory('.', 'users_info.txt')


if __name__ == '__main__':
    app.run(debug=True)