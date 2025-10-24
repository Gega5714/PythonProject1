# Contacts API Documentation

## Overview
The Contacts API allows users to manage their personal contact lists. Each user can create, read, update, and delete their contacts. The API also supports searching and filtering contacts based on various criteria.

## Authentication
The API uses token-based authentication. Users must authenticate to access their contacts.

## Endpoints

### 1. List Contacts
- **URL:** `/api/contacts/`
- **Method:** `GET`
- **Description:** Retrieve a list of contacts for the authenticated user.
- **Query Parameters:**
  - `search`: Optional. A string to search for in contact names or emails.
  - `filter`: Optional. A field to filter contacts (e.g., by category).

### 2. Create Contact
- **URL:** `/api/contacts/`
- **Method:** `POST`
- **Description:** Create a new contact for the authenticated user.
- **Request Body:**
  ```json
  {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "123-456-7890",
    "address": "123 Main St, Anytown, USA"
  }
  ```

### 3. Retrieve Contact
- **URL:** `/api/contacts/{id}/`
- **Method:** `GET`
- **Description:** Retrieve details of a specific contact by ID.

### 4. Update Contact
- **URL:** `/api/contacts/{id}/`
- **Method:** `PUT`
- **Description:** Update an existing contact for the authenticated user.
- **Request Body:**
  ```json
  {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "987-654-3210",
    "address": "456 Elm St, Othertown, USA"
  }
  ```

### 5. Delete Contact
- **URL:** `/api/contacts/{id}/`
- **Method:** `DELETE`
- **Description:** Delete a specific contact by ID.

## Response Format
All responses are returned in JSON format. Successful operations will return a status code of 200 (OK) or 201 (Created) along with the relevant data. Errors will return appropriate HTTP status codes and error messages.

## Error Handling
The API will return standard HTTP error codes for various issues:
- `400 Bad Request`: Invalid input data.
- `401 Unauthorized`: Authentication required.
- `403 Forbidden`: Access denied.
- `404 Not Found`: Contact not found.
- `500 Internal Server Error`: An unexpected error occurred.

## Conclusion
This API provides a robust way for users to manage their contacts. Ensure to authenticate before making requests and handle errors gracefully in your application.