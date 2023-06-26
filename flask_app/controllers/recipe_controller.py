from flask_app import app
from flask import render_template, redirect, request, session, flash, Flask
from flask_app.models.recipe_model import Recipe
from flask_app.models.user_model import User




################################################################################################################ <<GET/POST>> route to delete recipe
@app.route('/delete/<int:id>')
def delete_recipe(id):
    
    #has to be above session refrence below
    recipe = Recipe.view_one_recipe({'id':id})

    # if user doesn't match the creator of the recipe they don't have access to edit 
    if session["user_id"] != recipe.user_id:
        flash('User does not have access to this action')
        return redirect('/dashboard')
    
    
    #command to delet
    Recipe.delete({'id':id})


    return redirect('/dashboard')


################################################################################################################ <<GET>> route to have any user view a specific recipe
@app.route('/viewOne/<int:id>')
def show_recipe(id):
        if 'user_id' not in session:
            flash('Please login or Register', 'warning')
            return redirect('/')

        newUser = User.get_oneById({'id': session['user_id']})
        recipe = Recipe.view_one_recipe({"id":id})

        return render_template('viewRecipe.html', recipe=recipe, newUser=newUser)



################################################################################################################ <<GET>> route to VIEW add recipe page
@app.route('/newRecipe')
def newRecipePage():
        if 'user_id' not in session:
            flash('Please login or Register', 'warning')
            return redirect('/')

        newUser = User.get_oneById({'id': session['user_id']})

        return render_template('newRecipe.html', newUser=newUser)


################################################################################################################ <<POST>> route to SAVE add new recipe
@app.route('/newRecipe/add', methods=['POST'])
def addRecipe():
    # validate
    if not Recipe.validate_recipe(request.form):
        return redirect('/newRecipe')

    print(request.form)
    Recipe.save(request.form)
    return redirect('/dashboard')


################################################################################################################ <<GET>> route to VIEW edit recipe page
@app.route('/editRecipe/<int:id>')
def editRecipePage(id):
        if 'user_id' not in session:
            flash('Please login or Register', 'warning')
            return redirect('/')

        #has to be above session refrence below
        recipe = Recipe.view_one_recipe({'id':id})

        # if user doesn't match the creator of the recipe they don't have access to edit 
        if session["user_id"] != recipe.user_id:
            flash('User does not have access to this action')
            return redirect('/dashboard')
        
        #! print line below may be needed to troubleshoot, but may need to be changed to match new attribute
        # print(item.release_date)

        return render_template('editRecipe.html', recipe=recipe)


################################################################################################################ <<POST>> route to SAVE an edited recipe
@app.route('/editRecipe/edited/<int:id>', methods=['POST'])
def editRecipe(id):
        # validate
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/editRecipe/{id}')

    print(request.form)
    Recipe.update(request.form)
    return redirect('/dashboard')