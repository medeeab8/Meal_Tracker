## Introduction

My project is a Flask-based web application designed to manage meals and user profiles. It provides RESTful API endpoints for creating, updating, and deleting meals, as well as managing user accounts. The application is built using Flask, SQLAlchemy for database management, and other Python libraries.

### Features

- Allows users to add, update, delete meals, and manage their profiles.
- Calculates Total Daily Energy Expenditure (TDEE) based on user's height, weight, and activity level.
- Provides authentication and authorization mechanisms to ensure secure access to user data.
- Utilizes a relational database to store user profiles and meal information.

## Installation

To install the project locally, follow these steps:

1. Clone the repository from GitHub:

    ```
    git clone https://github.com/medeeab8/Meal_Tracker
    ```

2. Navigate to the project directory:

    ```
    cd Meal_Tracker
    ```

3. Create a virtual environment:

    ```
    python -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows: `venv\Scripts\activate`
    - On macOS and Linux: `source venv/bin/activate`

5. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

6. Set up the SQLite database:

    - **On Windows**: [Download SQLite](https://www.sqlite.org/download.html) and add it to your system's PATH.
    - **On Linux**: Run:

        ```
        sudo apt-get update
        sudo apt-get install sqlite3
        ```

7. Start the Flask development server:

    ```
    python run.py
    ```

## Usage

Once the project is installed, you can interact with the API using tools like cURL, Postman, or any HTTP client. Here are some example requests:

### Examples

- To add a meal:

    ```json
    POST /add_meal
    {
        "name": "Grilled Chicken Salad",
        "username": "john_doe",
        "description": "Grilled chicken breast with mixed greens",
        "calories": 350,
        "date": "2024-06-02"
    }
    ```

- To update a meal:

    ```json
    PUT /update_meal/<meal_id>
    {
        "username": "john_doe",
        "name": "Updated Chicken Salad",
        "description": "Updated description",
        "calories": 400,
        "date": "2024-06-03"
    }
    ```

- To get meals for a specific user:

    ```
    GET /meals/?username=john_doe
    ```

- To delete a meal:

    ```json
    DELETE /meals/<meal_id>
    {
        "meal_id": 1
    }
    ```

### Endpoints

- POST /add_meal: Add a new meal.
- PUT /update_meal/<meal_id>: Update an existing meal.
- GET /meals/: Get meals for a specific user.
- GET /get_meal/<meal_id>: Get details of a specific meal.
- DELETE /meals/<meal_id>: Delete a meal.
- POST /add_user: Add a new user.
- PUT /update_user/<user_id>: Update an existing user.
- DELETE /delete_user/<user_id>: Delete a user.
