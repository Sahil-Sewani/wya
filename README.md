# wya
## Shipment Tracking App

The Shipment Tracking App is a Flask-based web application designed to help users easily track their shipments. The app provides a user-friendly interface for authentication, allowing users to log in, view their personalized homepage, and add shipment tracking numbers for efficient monitoring.

## Features

- **User Authentication:**
  - Users can securely log in with their username and password.
  - New users can register and create an account.

- **Homepage:**
  - Upon successful login, users are greeted with a personalized homepage.
  - The homepage displays a welcome message along with any additional user-specific information.

- **Shipment Tracking:**
  - Users can add shipment tracking numbers to keep track of their packages.
  - The app utilizes a database to store user information and shipment details.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Flask JWT Extended
- Flask Bcrypt
- Flask CORS
- PyMySQL

## API Endpoints

The app provides the following API endpoints:

### `/login` (POST):

- User login endpoint.
- Requires a valid username and password.
- Returns a JSON web token upon successful login.

### `/register` (POST):

- User registration endpoint.
- Allows new users to create an account.

### `/add_package` (POST):

- Add shipment tracking number endpoint.
- No authentication required.
- Allows users to add a shipment tracking number for monitoring.

### `/get_packages` (GET):

- Get user's packages endpoint.
- Requires a valid JSON web token.
- Returns a list of packages associated with the authenticated user.

## HTML Webpages

### Login Page (`login.html`)

The login page provides a simple form for users to enter their credentials (username and password) to log in.

### Homepage (`home_page_3.html`)

The homepage is displayed upon successful login and features a welcome message along with any additional user-specific information. Users can also add shipment tracking numbers from this page.

## Database

### User Table

- `id`: User ID (Primary Key)
- `username`: User's username
- `password`: Hashed password

### Package Table

- `id`: Package ID (Primary Key)
- `package_name`: Name of the package
- `tracking_number`: Shipment tracking number
- `user_id`: Foreign key referencing the User table


