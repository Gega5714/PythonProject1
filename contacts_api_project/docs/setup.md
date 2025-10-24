# Setup Instructions for Contacts API Project

## Prerequisites
Before you begin, ensure you have the following installed on your machine:
- Python 3.6 or higher
- pip (Python package installer)
- Virtualenv (optional but recommended)

## Setting Up the Project

1. **Clone the Repository**
   Clone the project repository to your local machine using:
   ```
   git clone <repository-url>
   cd contacts_api_project
   ```

2. **Create a Virtual Environment**
   It is recommended to create a virtual environment to manage dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   Install the required packages listed in `requirements.txt`:
   ```
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the root directory of the project and copy the contents from `.env.example`. Update the values as necessary for your environment.

5. **Run Migrations**
   Apply the database migrations to set up the initial database schema:
   ```
   python manage.py migrate
   ```

6. **Create a Superuser (Optional)**
   If you want to access the Django admin interface, create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. **Run the Development Server**
   Start the development server to run the API:
   ```
   python manage.py runserver
   ```

8. **Access the API**
   You can access the API at `http://127.0.0.1:8000/`. Refer to `docs/api.md` for detailed API endpoint documentation.

## Additional Notes
- Ensure to check the `README.md` for more information about the project and its features.
- For testing, you can run:
  ```
  python manage.py test
  ```

This setup guide should help you get the Contacts API project up and running smoothly.