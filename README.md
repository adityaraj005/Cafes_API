# Cafe API

This project is a comprehensive RESTful API for managing cafe data, built using Flask and SQLAlchemy. The API supports CRUD operations, allowing users to create, read, update, and delete cafe records. It also includes robust security measures and has been tested using Postman.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete cafe records.
- **Security**: API key validation for sensitive operations.
- **Testing**: Utilized Postman for API testing and documentation.

## Technologies Used

- **Flask**: A micro web framework for Python.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **Postman**: API testing and documentation tool.

## Endpoints

### GET

- `/random`: Get a random cafe.
- `/all`: Get all cafes.
- `/search`: Search for cafes by location.

### POST

- `/add`: Add a new cafe.

### PATCH

- `/update-price/<cafe_id>`: Update the price of a cafe.

### DELETE

- `/report-closed/<cafe_id>`: Delete a cafe (requires API key).

## Database Schema

The `Cafe` table includes the following columns:

- `id`: Integer, primary key.
- `name`: String, unique, not nullable.
- `map_url`: String, not nullable.
- `img_url`: String, not nullable.
- `location`: String, not nullable.
- `seats`: String, not nullable.
- `has_toilet`: Boolean, not nullable.
- `has_wifi`: Boolean, not nullable.
- `has_sockets`: Boolean, not nullable.
- `can_take_calls`: Boolean, not nullable.
- `coffee_price`: String, nullable.

## Usage

1. Install the required packages using `pip install -r requirements.txt`.
2. Run the Flask application using `python app.py`.
3. Use Postman or any other API client to interact with the endpoints.
