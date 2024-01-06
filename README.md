FastAPI Book Inventory
This project provides a simple Book Inventory system with REST APIs built using FastAPI.

User Registration API
Register a new user
Method: POST
Endpoint: /api/user/register
Request Body:
Name (string)
Email (string)
Password (string)

User Login API
Authenticate and get an access token
Method: POST
Endpoint: /api/user/login
Request Body:
Email (string)
Password (string)

Book APIs
Create Book (Admin Only)
Method: POST
Endpoint: /api/book
Request Body:
Title (string)
Description (string)
Author (string)
Count (integer)

Get All Books
Method: GET
Endpoint: /api/book

Get Book by ID
Method: GET
Endpoint: /api/book/{book_id}

Update Book (Admin Only)
Method: PUT
Endpoint: /api/book/{book_id}
Request Body:
Title (string)
Description (string)
Author (string)
Count (integer)

Delete Book (Admin Only)
Method: DELETE
Endpoint: /api/book/{book_id}

