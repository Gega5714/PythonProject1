# Contacts API Project

This project is a Django Rest Framework application that provides a Contacts API. Each user has their own list of contacts, with functionality to search, filter, and update contacts.

## Features

- User authentication and management
- CRUD operations for contacts
- Search and filter capabilities for contacts
- API documentation

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd contacts_api_project
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env` and fill in the necessary configurations.

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

## Usage

- The API endpoints can be accessed at `http://localhost:8000/api/`.
- Use tools like Postman or curl to interact with the API.

## API Documentation

Refer to the `docs/api.md` file for detailed API documentation.

## Testing

To run tests, use the following command:
```
python manage.py test
```

## License

This project is licensed under the MIT License.