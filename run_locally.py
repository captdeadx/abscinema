#!/usr/bin/env python3
"""
ABS Cinema - Local Hosting Setup Script
This script sets up the environment and runs the Flask application locally.

Usage:
    python run_locally.py

Requirements:
    - Python 3.6+
    - Flask
    - SQLite3
"""
import os
import sys
import sqlite3
import subprocess
import shutil
import time

# Check Python version
if sys.version_info < (3, 6):
    print("Error: Python 3.6 or higher is required")
    sys.exit(1)

try:
    import flask
except ImportError:
    print("Installing Flask...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    import flask

# Constants
DB_NAME = "abs_cinema.db"
APP_FILE = "app.py"
TEMPLATES_DIR = "templates"
STATIC_DIR = "static"
USERS_FILE = "users_info.txt"


def setup_directory():
    """Create necessary directories"""
    print("Setting up directory structure...")

    # Create templates directory if it doesn't exist
    if not os.path.exists(TEMPLATES_DIR):
        os.makedirs(TEMPLATES_DIR)
        print(f"Created {TEMPLATES_DIR} directory")

    # Create static directory if it doesn't exist
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)
        print(f"Created {STATIC_DIR} directory")

    # Ensure we have a copy of the cinema.html file in static for direct access
    if os.path.exists(os.path.join(TEMPLATES_DIR, "cinema.html")):
        shutil.copy(
            os.path.join(TEMPLATES_DIR, "cinema.html"),
            os.path.join(STATIC_DIR, "cinema.html")
        )
        print("Copied cinema.html to static directory")


def initialize_database():
    """Initialize the SQLite database"""
    print("Initializing database...")

    # Check if the database file exists and remove it if it does
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"Removed existing {DB_NAME}")

    # Create a new database connection
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

    seat_id = 1
    for cinema in cinemas:
        for movie in movies:
            for show_time in show_times:
                cursor.execute(
                    "INSERT INTO cinema_seats (id, cinema_name, movie_name, show_time, total_seats, booked_seats) VALUES (?, ?, ?, ?, 500, 0)",
                    (seat_id, cinema, movie, show_time)
                )
                seat_id += 1

    # Initialize users
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

    print(f"Database {DB_NAME} initialized successfully")


def create_users_info_file():
    """Create the users_info.txt file with credentials"""
    print("Creating users info file...")

    with open(USERS_FILE, 'w') as file:
        file.write("CINEMA BOOKING SYSTEM - USER CREDENTIALS\n")
        file.write("=====================================\n\n")
        file.write("Regular Users:\n")
        file.write("1. Username: user1, Password: password123\n")
        file.write("2. Username: user2, Password: Pass22\n")
        file.write("3. Username: user3, Password: Pass33\n")
        file.write("4. Username: user4, Password: Pass44\n\n")
        file.write("Administrator:\n")
        file.write("Username: admin, Password: @dM!N\n\n")
        file.write("Note: This file is accessible via URL, demonstrating path traversal vulnerability.\n\n")
        file.write("Database Details:\n")
        file.write("- Database Name: abs_cinema\n")
        file.write("- Tables:\n")
        file.write("  1. cinema_seats - Stores seat information for each cinema/movie/time\n")
        file.write("  2. bookings - Stores all booking details\n")
        file.write("  3. users - Stores user credentials\n\n")
        file.write("URL Tampering Examples:\n")
        file.write("- To access admin panel: ?adminMode=true\n")
        file.write("- To impersonate another user: ?userId=2&isAdmin=true\n")
        file.write("- To book more than 15 seats: ?attendees=600\n\n")
        file.write("For educational purposes only. Do not use these vulnerabilities in production environments.\n")

    print(f"Created {USERS_FILE}")


def run_flask_app():
    """Run the Flask application"""
    print("Starting the Flask application...")

    try:
        # Check if app.py exists
        if not os.path.exists(APP_FILE):
            print(f"Error: {APP_FILE} not found.")
            sys.exit(1)

        print("\n------------------------------------------------------")
        print("ABS Cinema Booking System Started")
        print("------------------------------------------------------")
        print(f"- Local URL: http://127.0.0.1:5000/")
        print("- Username: user1, Password: password123")
        print("- Admin: admin, Password: @dM!N")
        print("------------------------------------------------------")
        print("Press Ctrl+C to stop the server")
        print("------------------------------------------------------\n")

        # Run the Flask application
        subprocess.run([sys.executable, APP_FILE])

    except KeyboardInterrupt:
        print("\nApplication stopped")
    except Exception as e:
        print(f"Error running Flask application: {e}")


def main():
    """Main function to setup and run the application"""
    print("\n==== ABS Cinema Booking System Setup ====\n")

    setup_directory()
    initialize_database()
    create_users_info_file()

    # Small delay for setup to complete
    time.sleep(1)

    run_flask_app()


if __name__ == "__main__":
    main()