# Overview

This project is a FastAPI microservice that provides secure login functionality for both admin and user roles, leveraging dynamic Role-Based Access Control (RBAC) through the Oso framework. Additionally, it integrates Retrieval-Augmented Generation (RAG) for enhanced question-answering capabilities using OpenAI's GPT models. The service also supports PDF document uploads, text extraction, and embedding generation for advanced querying.

## Postman Collection

A Postman collection is included to test the API endpoints. You can find the collection file at:

```
Postman Collection/fastapi-rbac-microservice.postman_collection.json
```

To use the collection:

1. Open Postman.
2. Import the collection file by navigating to `File > Import` and selecting the JSON file.
3. Update the environment variables in Postman (e.g., `base_url`, `token`) to match your local setup.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)
- A database (SQLite is used by default, but you can configure another database in the `.env` file)

## Features

- **Secure Authentication**: Supports JWT-based authentication for users and admins.
- **Role-Based Access Control (RBAC)**: Implements dynamic RBAC using the Oso framework.
- **Retrieval-Augmented Generation (RAG)**: Integrates OpenAI's GPT models for question-answering with context from uploaded documents.
- **PDF Upload and Processing**: Allows admins to upload PDFs, extract text, generate embeddings, and save them for querying.
- **Modular Architecture**: Designed for easy maintenance and scalability.

## Database Initialization

To initialize the database, run the following command:

```
python initialize_db.py
```

This will create the necessary tables in the database.

## Creating an Admin User

To create an admin user, execute the following script:

```
python create_admin.py
```

The default admin credentials are:

- Username: `admin`
- Password: `admin`

You can modify these credentials in the `create_admin.py` file before running the script.

## Environment Variables

The application uses a `.env` file to manage environment variables. Below is an example of the `.env` file:

```
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
RBAC_POLICY_PATH=app/rbac/policies.polar
OPENAI_API_KEY=your_openai_api_key
```

Replace `your_secret_key` and `your_openai_api_key` with your actual values.

## API Documentation

The API documentation is automatically generated and available at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

These provide detailed information about the available endpoints, request/response formats, and authentication requirements.

## Project Structure

```
fastapi-rbac-microservice
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── auth
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── utils.py
│   ├── rbac
│   │   ├── __init__.py
│   │   ├── policies.polar
│   │   └── oso.py
│   ├── users
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── admin
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── schemas.py
│   └── services
│       ├── embedding_service.py
├── requirements.txt
├── .env
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd fastapi-rbac-microservice
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables in the `.env` file.

## Usage

To run the FastAPI application, execute the following command:
```
uvicorn app.main:app --reload
```

You can access the API documentation at `http://127.0.0.1:8000/docs`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.# Overview
