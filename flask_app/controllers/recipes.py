from flask import render_template, redirect, request, session, url_for
from flask_app import app
from flask_app.models.recipe import Recipe

@app.route('/recipes')
def display_recipes():
    # User must be logged in to view this page
    if 'logged_in_user_id' not in session:
        return redirect(url_for('display_reg_login'))
    all_recipes = Recipe.get_all_with_users()
    return render_template('display_recipes.html', recipes=all_recipes)

@app.route('/recipes/<int:recipe_id>')
def display_one_recipe(recipe_id):
    # User must be logged in to view this page
    if 'logged_in_user_id' not in session:
        return redirect(url_for('display_reg_login'))
    one_recipe = Recipe.get_one_with_user(recipe_id)
    return render_template('display_one_recipe.html', recipe=one_recipe)

@app.route('/recipes/new', methods=['GET', 'POST'])
def create_recipe():
    # User must be logged in to view this page
    if 'logged_in_user_id' not in session:
        return redirect(url_for('display_reg_login'))

    if request.method == 'GET':
        return render_template('add_recipe.html')
    elif request.method =='POST':
        if not Recipe.validate_recipe(request.form):
            session['create_recipe_data'] = request.form
            return redirect(url_for('create_recipe'))
        # If form passes validation, create recipe and remove create_recipe_data from session
        if 'create_recipe_data' in session:
            session.pop('create_recipe_data')
        Recipe.create(request.form)
        return redirect(url_for('display_recipes'))

@app.route('/recipes/edit/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    # User must be logged in to view this page
    if 'logged_in_user_id' not in session:
        return redirect(url_for('display_reg_login')) 
    
    if request.method == 'GET':
        one_recipe = Recipe.get_one_with_user(recipe_id)
        return render_template('edit_recipe.html', recipe=one_recipe)
    elif request.method == 'POST':
        if not Recipe.validate_recipe(request.form):
            return redirect(f'/recipes/edit/{recipe_id}')
        Recipe.update(request.form)
        return redirect(url_for('display_recipes'))
    
@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    # User must be logged in to delete a recipe
    if 'logged_in_user_id' not in session:
        return redirect(url_for('display_reg_login'))
    Recipe.delete_by_id(recipe_id)
    return redirect(url_for('display_recipes'))