from fastapi import FastAPI, HTTPException, Query
from api_handler import ApiHandler
from database_handler import DatabaseHandler
import credentials

app = FastAPI()

class RecipeMaker:
    """A class for interacting with the Edamam API and storing recipes in MongoDB."""

    def __init__(self, api_id, api_key, db_connection_string, db_name, collection_name):
        """Initialize the RecipeMaker with API credentials and MongoDB connection."""
        self.api_id = api_id
        self.api_key = api_key
        self.api_handler = ApiHandler()
        self.db_handler = DatabaseHandler(db_connection_string, db_name, collection_name)

    def get_recipe(self, ingredients):
        """Get a recipe from the Edamam API."""
        try:
            data = self.api_handler.get_recipe(ingredients, self.api_id, self.api_key)

            if 'hits' in data and data['hits']:
                recipe = data['hits'][0]['recipe']
                label = recipe.get('label', 'No label available')
                time = recipe.get('totalTime', 0)
                url = recipe.get('url', 'No URL available')

                # Try different keys for preparation
                possible_preparation_keys = ['instructions', 'preparation', 'directions']
                for preparation_key in possible_preparation_keys:
                    preparation = recipe.get(preparation_key)
                    if preparation:
                        break
                else:
                    preparation = 'No preparation available'

                category = recipe.get('category', 'Uncategorized')

                recipe_data = {
                    "label": label,
                    "time": time,
                    "url": url,
                    "preparation": preparation,
                    "category": category
                }

                inserted_id = self.db_handler.insert_recipe(recipe_data)

                # Retrieve the inserted recipe using the ID
                inserted_recipe = self.db_handler.get_recipe_by_id(inserted_id)

                return {
                    "recipe": inserted_recipe["label"],
                    "total_cooking_time": inserted_recipe["time"],
                    "url": inserted_recipe["url"],
                    "preparation": inserted_recipe["preparation"],
                    "category": inserted_recipe["category"]
                }
            else:
                raise HTTPException(status_code=404, detail="No recipe found for the given ingredients.")
        except Exception as e:
            import traceback
            traceback.print_exc()  # Print the traceback for debugging
            raise HTTPException(status_code=500, detail=str(e))

recipe_maker = RecipeMaker(credentials.API_ID, credentials.API_KEY,
                           "mongodb+srv://MY_USERNAME:MY_PASSWORD@MYCLUSTER.dlrkkr2.mongodb.net/?retryWrites=true&w=majority",
                           "recipes", "recipe_collection")

# Expose the recipe_maker instance as an attribute of the FastAPI app
app.state.recipe_maker = recipe_maker

@app.get("/get_recipe/")
async def get_recipe(ingredients: str = Query(..., title="Ingredients", description="Comma-separated list of ingredients")):
    """Get a recipe based on ingredients."""
    try:
        return app.state.recipe_maker.get_recipe(ingredients.split(','))
    except HTTPException as e:
        raise e  # Re-raise HTTPException to let FastAPI handle HTTP errors
    except Exception as e:
        import traceback
        traceback.print_exc()  # Print the traceback for debugging
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
