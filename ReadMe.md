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

## Quick Start with Docker

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup and Run

1. Clone the repository or download the project files:

```bash
git clone <repository-url>
cd abs_cinema
```

2. Make sure you have the following file structure:

```
abs_cinema/
├── app.py                  # Flask application
├── Dockerfile              # Docker build instructions
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── templates/
│   ├── index.html          # Directory index page
│   └── cinema.html         # Main cinema booking application
└── static/                 # Static files (optional)
```

3. Build and start the Docker container:

```bash
docker-compose up --build
```

4. Access the application:
   - Main application: http://localhost:5000/
   - Directory index (requires URL manipulation): http://localhost:5000/index

## Docker Commands

Here are useful commands for managing your Docker container:

```bash
# Build and start the containers
docker-compose up --build

# Run containers in the background
docker-compose up -d

# Stop the containers
docker-compose down

# View logs
docker-compose logs -f

# Restart the containers
docker-compose restart

# Check container status
docker-compose ps

# Access the container shell
docker-compose exec cinema-app bash
```


## Data Persistence

The application uses a Docker volume to persist data:
- Database file: `data/abs_cinema.db`
- User credentials file: `data/users_info.txt`

This ensures your data survives container restarts.

## Troubleshooting

- **Permission Issues**: If you encounter permission problems with the data directory:
  ```bash
  sudo chown -R $USER:$USER abs_cinema/data
  ```

- **Port Conflict**: If port 5000 is already in use, modify the port mapping in `docker-compose.yml`:
  ```yaml
  ports:
    - "8080:5000"  # Change 5000 to any available port
  ```

## Educational Use

This application is designed to demonstrate:
- Common web security vulnerabilities
- How attackers can exploit insecure design
- The importance of proper input validation
- Secure session management practices

Remember that this is a deliberately vulnerable application. Never use this code in a production environment or expose it to the internet.