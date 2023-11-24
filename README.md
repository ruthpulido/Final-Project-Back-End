# Cook-Eat-App

This is a simple FastAPI application named Cook-Eat-App / RecipeMaker. It interacts with the Edamam API to fetch recipes based on provided ingredients and stores them in a MongoDB database.

# Installation
Before running the application, make sure to install the required dependencies. You can do this using:

pip install -r requirements.txt

# Configuration
To run the application, you need to provide your Edamam API credentials and MongoDB connection string from the main.py file. Create a credentials.py file and include the following:

        # credentials.py
        API_ID = "my_edamam_api_id"
        API_KEY = "my_edamam_api_key"

# Running the Application
To start the Cook-Eat-App / RecipeMaker app, run the following command:

    python main.py

The application will be accessible at http://127.0.0.1:8001/docs Visit this URL in your browser or use an API testing tool like Swagger UI to interact with the API.

## API Endpoint
Get Recipe
* Endpoint: /get_recipe/
* Method: GET
* Parameters:
    * ingredients (query parameter): Comma-separated list of ingredients.
* Response:
    * Returns details of a recipe based on the provided ingredients.
    * If no recipe is found, a 404 error is returned.
    * In case of any internal error, a 500 error is returned.