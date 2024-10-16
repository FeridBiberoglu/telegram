# Profitsniffer Backend

This backend service is built using FastAPI, `Motor` (async MongoDB driver), and `Uvicorn` for running the application. It is part of the **Profitsniffer** project and uses `Pipenv` for managing dependencies.

## Technologies Used

- **FastAPI**: A modern web framework for building APIs with Python 3.7+ based on standard Python-type hints.
- **Motor**: An async MongoDB driver for Python, allowing non-blocking database access with FastAPI.
- **Uvicorn**: ASGI server for running FastAPI applications.
- **Pipenv**: Dependency and virtual environment manager for Python.

## Prerequisites

Ensure that you have the following installed on your machine:

- Python 3.12+
- Pipenv
- MongoDB (or access to a MongoDB database)

## Setup and Installation

If you have just cloned this repository, follow these steps to set up the backend environment:

1. **Install Pipenv**: Ensure you have `pipenv` installed by running:

   ```bash
   python3 -m pip install pipenv
   ```

2. **Install Dependencies**: Navigate to the `backend` directory and install the project dependencies from `requirements.txt` using `pipenv`:

   ```bash
   cd backend
   pipenv install -r requirements.txt
   ```

   This will create a virtual environment and install all necessary dependencies, including FastAPI and Motor.

3. **Activate the Virtual Environment**:

   After installing the dependencies, activate the virtual environment:

   ```bash
   pipenv shell
   ```

   You will now be inside the virtual environment, where you can run all commands for the backend.

## MongoDB Setup

The backend relies on MongoDB for data storage. Ensure that MongoDB is installed locally or you have access to a MongoDB instance.

### MongoDB Configuration

You need to set up the MongoDB connection string in the `.env` file located in the `backend` directory. Here's an example of what it should look like:

```
MONGO_URI=mongodb://localhost:27017/yourdbname
```

Replace `yourdbname` with your actual MongoDB database name. If you're using MongoDB Atlas or a remote MongoDB instance, update the `MONGO_URI` accordingly.

## Scripts

This project includes the following useful scripts:

- **Run FastAPI Development Server**: To start the backend API server in development mode, run:

  ```bash
  uvicorn app.main:app --reload
  ```

  This command launches the FastAPI app on `http://localhost:8000` and reloads automatically when code changes are detected.

- **Test the API**: You can test the API by visiting `http://localhost:8000` in your browser or using a tool like `curl` or Postman.

- **Update Dependencies**: You can update the `requirements.txt` file with the current environment’s dependencies by running:

  ```bash
  pipenv lock -r > requirements.txt
  ```

## Running the API

To start the backend API in development mode:

```bash
uvicorn app.main:app --reload
```

This command runs the API server with auto-reload enabled, which means any code changes will automatically restart the server.

## Project Structure

The project structure follows a standard FastAPI setup, with additional MongoDB integration using Motor:

```
backend/
├── app/
│   ├── __init__.py            # Initialize the FastAPI app
│   ├── main.py                # Main entry point for FastAPI
│   ├── routers/               # API routes
│   │   └── example_route.py    # Example API routes
│   ├── db/                    # MongoDB connection setup
│   │   └── mongo.py           # Motor client setup for MongoDB
│   └── models/                # Pydantic models
│
├── Pipfile                    # Pipenv environment file
├── Pipfile.lock               # Locked dependencies for pipenv
└── requirements.txt           # Dependency list for pip installations
```

## Environment Variables

The project uses a `.env` file to configure environment-specific settings like MongoDB credentials and other sensitive information.

Create a `.env` file in the `backend` directory and add your environment variables there. Example:

```
MONGO_URI=mongodb://localhost:27017/yourdbname
SECRET_KEY=your_secret_key
```

## Deploy

To deploy this FastAPI app, you can use platforms like Heroku, DigitalOcean, or any cloud provider that supports Python apps. Make sure to set the environment variables correctly in your deployment environment.

## Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Motor Documentation](https://motor.readthedocs.io/en/stable/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Pipenv Documentation](https://pipenv.pypa.io/en/latest/)

---
