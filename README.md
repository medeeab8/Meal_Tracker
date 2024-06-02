1. Introduction
My project is a Flask-based web application designed to manage meals and user profiles. It provides RESTful API endpoints for creating, updating, and deleting meals, as well as managing user accounts. The application is built using Flask, SQLAlchemy for database management, and other Python libraries.

2. Features
Allows users to add, update, delete meals, and manage their profiles.
Calculates Total Daily Energy Expenditure (TDEE) based on user's height, weight, and activity level.
Provides authentication and authorization mechanisms to ensure secure access to user data.
Utilizes a relational database to store user profiles and meal information.

3. Installation
To install the project locally, follow these steps:

Clone the repository from GitHub:
git clone https://github.com/medeeab8/Meal_Tracker

Navigate to the project directory:
cd Meal_Tracker

Create a virtual environment:
python -m venv venv

1. Activate the virtual environment:

On Windows:
venv\Scripts\activate

On macOS and Linux:
source venv/bin/activate

2. Install dependencies:
pip install -r requirements.txt

3. Set up the SQLite database:

On Windows:
Visit the SQLite website: https://www.sqlite.org/download.html
Under the "Precompiled Binaries for Windows" section, download the appropriate version (either 32-bit or 64-bit) depending on your system architecture.
Extract the downloaded ZIP file.
Copy the sqlite3.exe file to a directory included in your system's PATH environment variable. Common directories include C:\Windows or C:\Windows\System32.

On Linux:
Open a terminal.
Run the following commands:
sudo apt-get update
sudo apt-get install sqlite3
This will install SQLite3 along with its command-line interface.

4. Start the Flask development server:
python run.py

4. Usage
Once the project is installed, you can interact with the API using tools like cURL, Postman, or any HTTP client. Here are some example requests:

When making POST requests to the API endpoints that expect JSON data, ensure that the following headers are set:

- **Content-Type**: Should be set to `application/json`. This informs the server that the request body contains JSON data.

- **Content-Length**: This header should contain the length of the JSON data being sent. It's important for the server to accurately determine the size of the incoming data.

Examples: 

To add a meal:
POST /add_meal
{
    "name": "Grilled Chicken Salad",
    "username": "john_doe",
    "description": "Grilled chicken breast with mixed greens",
    "calories": 350,
    "date": "2024-06-02"
}

To update a meal:
PUT /update_meal/<meal_id>
{
    "username": "john_doe",
    "name": "Updated Chicken Salad",
    "description": "Updated description",
    "calories": 400,
    "date": "2024-06-03"
}

To get a meal by username:
GET /meals/<username>
{
  "username": "john_doe"
}

To delete a meal:
DELETE meals/<int:id>
{
  "meal_id": 1
}

To add a user:
POST add_user 
{
  "username": "newuser",
  "height": 170,
  "weight": 70,
  "activity_level": 3
}


5. Endpoints

POST /add_meal: Add a new meal.
PUT /update_meal/<meal_id>: Update an existing meal.
GET /meals/<username>: Get meals for a specific user.
GET/get_meal/<meal_id>: Get details of a specific meal.
DELETE /meals/<meal_id>: Delete a meal.
POST/add_user: Add a new user.
PUT /update_user/<user_id>: Update an existing user.
DELETE /delete_user/<user_id>: Delete a user.
