# ABS Cinema Booking System

A deliberately vulnerable cinema booking web application for security testing and education. This application contains several intentional security vulnerabilities to demonstrate common web security issues.

## Security Vulnerabilities Demonstrated

This application includes the following vulnerabilities:

1. **SQL Injection** - The login system and several other database queries are intentionally vulnerable to SQL injection.
2. **URL Tampering** - Parameters in URLs can be modified to change booking details, seat counts, etc.
3. **Insecure Direct Object References (IDOR)** - Users can access each other's bookings by manipulating IDs.
4. **Insecure Design** - No proper validation on number of attendees, allowing overbooking.
5. **Path Traversal** - Sensitive files like user credentials are accessible via direct URL.

## Setup Instructions

### Prerequisites

- Python 3.6 or higher
- SQLite3 (included with Python)
- Flask (will be installed by the setup script if not present)

### Quick Start

1. Clone or download this repository to your local machine.

2. Run the setup script:
   ```bash
   python run_locally.py
   ```
   This will:
   - Create necessary directories
   - Initialize the SQLite database
   - Create sample data
   - Start the Flask application

3. Access the application at:
   ```
   http://127.0.0.1:5000/
   ```

### Sample Users

| Username | Password    | Role      |
|----------|-------------|-----------|
| user1    | password123 | Regular   |
| user2    | Pass22      | Regular   |
| user3    | Pass33      | Regular   |
| user4    | Pass44      | Regular   |
| admin    | @dM!N       | Admin     |

## Database Structure

The application uses an SQLite database named `abs_cinema.db` with the following tables:

1. **cinema_seats** - Information about available seats in each theater
   - id, cinema_name, movie_name, show_time, total_seats, booked_seats

2. **bookings** - Details of all bookings made
   - id, booking_id, user_id, cinema_name, movie_name, show_time, attendees, total_price, discount, final_price, booking_time, is_admin_booking

3. **users** - User accounts
   - id, username, password, is_admin

## Disclaimer

This application is intended for educational purposes only. The vulnerabilities included are deliberately implemented to demonstrate security concepts. Do not use this code in production environments or expose it to public networks.