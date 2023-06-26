from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

#import the module (for importing into models)
from flask_app.models import user_model

# contructs the show object (below)
# update Class name*
class Recipe:
    # **<<ADD SCHEMA DB NAME HERE>>**
    # CHANGE BELOW TO MATCH NEWLY NAMED DB
    DB = 'test_recipes3_db'

    # May need to update list below based on erd diagram
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_30_minutes = data['under_30_minutes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None


################################################################################################################ <<Staticmethod>> to validate edit / add new recipe - update categories
# update category flash filter & update title, network, release_date, description fields
    @staticmethod
    def validate_recipe(verify_recipe):
        is_valid = True
        if len(verify_recipe['name']) < 1:
            flash('Name must be 1 charecter or more!', 'val_recipe')
            is_valid = False
        if len(verify_recipe['description']) < 2:
            flash('Description must be 1 charecter or more!', 'val_recipe')
            is_valid = False
        if len(verify_recipe['instructions']) < 1:
            flash('Instructions must be added!', 'val_recipe')
            is_valid = False
        if len(verify_recipe['date_cooked']) < 4:
            flash('Date cooked must be added!', 'val_recipe')
            is_valid = False
        if 'under_30_minutes' not in verify_recipe:
            flash('Selection must be made!', 'val_recipe')
            is_valid = False
        
        return is_valid
    



################################################################################################################ <<Classmethod>> to save a submitted new Recipe by adding it to our DB
# update query to match newly named fields*
#!may need to verify date field and under 30 minutes field*
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO recipes (name, description, instructions, date_cooked, under_30_minutes, user_id)
        VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_30_minutes)s, %(user_id)s);
        """

        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
    


################################################################################################################ JOIN <<Classmethod>> to get all recipes from all users
    #! update query based on new name of table (item, recipes, shows, books, etc...)
    @classmethod
    def get_all_recipes(cls):
        query = """
        SELECT * 
        FROM recipes
        JOIN users ON recipes.user_id = users.id;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        # use to check if working...
        print(results)

        all_recipes = []

        for recipe_from_db in results:
            one_recipe = cls(recipe_from_db) 

            # update userData if user has additional categories from its table on the erd
            userData = {
                "id" : recipe_from_db["users.id"],
                "first_name" : recipe_from_db["first_name"],
                "last_name" : recipe_from_db["last_name"],
                "email" : recipe_from_db["email"],
                "password" : recipe_from_db["password"],
                "created_at" : recipe_from_db["users.created_at"],
                "updated_at" : recipe_from_db["users.updated_at"],
                }
            one_recipe.creator = user_model.User(userData)
            all_recipes.append(one_recipe)

        return all_recipes

#side note - - USE in jinja for view show page one_show.creator.first_name


################################################################################################################ <<Classmethod>> to view one recipe
    # update query based on new name of table (item, shows, books, recipes, etc.)
    @classmethod
    def view_one_recipe(cls, data):
        query="""SELECT * FROM recipes
        LEFT JOIN users
        ON recipes.user_id = users.id
        WHERE recipes.id = %(id)s;        
        """


        results = connectToMySQL(cls.DB).query_db(query, data)

        singleRecipe = cls(results[0])

        # user data fields may need to be updated if there's more or different field names in the user class*
        userData = {
            "id" : results[0]["users.id"],
            "first_name" : results[0]["first_name"],
            "last_name" : results[0]["last_name"],
            "email" : results[0]["email"],
            "password" : results[0]["password"],
            "created_at" : results[0]["users.created_at"],
            "updated_at" : results[0]["users.updated_at"]
        }
        singleRecipe.creator = user_model.User(userData)
            
        return singleRecipe
    


################################################################################################################ <<Classmethod>> to update recipe
    # may need to update query fields based on the table name and categories 
    @classmethod
    def update(cls, data): 
        query = """
        UPDATE recipes
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_cooked = %(date_cooked)s, under_30_minutes = %(under_30_minutes)s
        WHERE id = %(id)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
    

################################################################################################################ <<Classmethod>> to delete a recipe
    # may need to update query fields
    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM recipes
        WHERE id = %(id)s
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result


#################################################################################################### <<classmethod>> to get one item (via id)
    # may need to update function name & query fields
    @classmethod
    def get_oneRecipeById(cls,data):
        query = """
        SELECT * 
        FROM recipes
        WHERE id = %(id)s;
        """    

        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])