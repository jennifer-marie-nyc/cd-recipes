from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from datetime import datetime

class Recipe:
    db = 'recipes_schema'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_30 = data['under_30']
        self.user_id = data['user_id']
        self.creator = None
        
    @staticmethod
    def create(form_data):
        query = """
            INSERT INTO recipes
            (name, description, instructions, date_cooked, under_30, user_id)
            VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_30)s, %(user_id)s);
        """
        connectToMySQL('recipes_schema').query_db(query, form_data)

    @staticmethod
    def validate_recipe(form_data):
        is_valid = True
        print('Validating recipe...')

    # Validate recipe name
        if len(form_data['name'].strip()) == 0:
            flash('Recipe name is required')
            is_valid = False
        elif len(form_data['name'].strip()) < 3:
            flash('Recipe name must be at least 2 characters.')
            is_valid = False

    # Validate description
        if len(form_data['description'].strip()) == 0:
            flash('Description is required')
            is_valid = False
        elif len(form_data['description'].strip()) < 3:
            flash('Description must be at least 2 characters.')
            is_valid = False

    # Validate instructions
        if len(form_data['instructions'].strip()) == 0:
            flash('Instructions is required')
            is_valid = False
        elif len(form_data['instructions'].strip()) < 3:
            flash('Instructions must be at least 2 characters.')
            is_valid = False

    # Validate date cooked
        if not form_data['date_cooked']:
            flash('Date cooked is required')
            is_valid = False
        # If date cooked entered, contintue with other birthday validation checks
        else:
            # Date cooked must be in the past
            date_cooked = datetime.strptime(form_data['date_cooked'], '%Y-%m-%d').date()
            today = datetime.today().date()
            if date_cooked > today:
                flash('Date cooked cannot be in the future')
                is_valid = False

    # Validate under 30 minutes
        # if form_data['under_30'] != 0 or form_data['under_30'] != 1:
        if 'under_30' not in form_data:
            flash('Under 30 minutes is required')
            is_valid = False
        
        return is_valid


    @staticmethod
    def update(form_data):
        query = """
            UPDATE recipes
            SET name = %(name)s,
            description = %(description)s,
            instructions = %(instructions)s,
            date_cooked = %(date_cooked)s,
            under_30 = %(under_30)s
            WHERE id = %(id)s
        """
        connectToMySQL('recipes_schema').query_db(query, form_data)

    @staticmethod
    def delete_by_id(recipe_id):
        query = 'DELETE FROM recipes where id = %(id)s'

        data = {
            'id': recipe_id
        }

        connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def get_one_with_user(cls, recipe_id):
        query = """
            SELECT * FROM recipes
            LEFT JOIN users
            ON recipes.user_id = users.id
            WHERE recipes.id = %(recipe_id)s;
        """
        data = {
            'recipe_id': recipe_id
        }
        results = connectToMySQL(cls.db).query_db(query, data)
        one_dict = results[0]
        one_recipe = cls(one_dict)

        user_data = {
                'id': one_dict['users.id'],
                'first_name': one_dict['first_name'],
                'last_name': one_dict['last_name'],
                'email': one_dict['email']
            }
        
        user_obj = User(user_data)

        one_recipe.creator = user_obj

        return one_recipe

    @classmethod
    def get_all_with_users(cls):
        query = """
            SELECT * FROM recipes
            LEFT JOIN users
            ON recipes.user_id = users.id;
        """
        results = connectToMySQL(cls.db).query_db(query)

        all_recipes = []

        for row in results:
            recipe = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email']
            }
            user_obj = User(user_data)
            recipe.creator = user_obj
            all_recipes.append(recipe)

        return all_recipes