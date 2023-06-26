from flask import render_template, redirect, request, session, flash
from flask_app import app

from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

from flask_bcrypt import Bcrypt  # Only needed on routes related to login/reg
bcrypt = Bcrypt(app)

# Import Your Models as Classes into the Controller to use their Classmethods

# from flask_app.models.table_model import classname


################################################################################################################ Home Route
@app.route('/')
def login_home():
    return render_template("login.html")


################################################################################################################ <<POST>> Route to register new user
@app.route('/register_new_user', methods=['POST'])
def register_new_user():
    #go back to home is not a registered user or info is wrong
    if not User.validate_new_user(request.form):
        return redirect('/')
    
    # may need to add at end of thread above: ".decode('utf-8')"
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    #adjust based on table (auto fields are id, create, updated - don't need to be added)
    newUser_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    #make the user
    user_id = User.save_new_user(newUser_data)
    
    #putting user into session
    session['user_id'] = user_id

    #successfully taken to dashboard to see all shows
    return redirect(f'/dashboard')


################################################################################################################ <<POST>> Route for login validation check for user login 
@app.route('/login_user', methods=['POST'])
def validate_login():

    #check if email exists in db
    login_data = {'email':request.form['email']}
    user_in_db = User.get_oneByEmail(login_data)

    if not user_in_db: 
        #flash messages have category*
        flash('Invalid Email/Password', 'login')
        return redirect('/')

    # check if unhashed pw correct
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/')

    #if valid then progress...    
    session['user_id'] = user_in_db.id
    
    return redirect('/dashboard')


################################################################################################################ <<GET>> Route to successful login / Transfers user to dashboard page
@app.route('/dashboard')
def show_dashboard():

        if 'user_id' not in session:
            flash('Please login or Register', 'warning')
            return redirect('/')
        
        # newUser == name to refer to on jinja on html
        newUser = User.get_oneById({'id': session['user_id']})

        # added to show all the recipes on dashboard
        all_recipes = Recipe.get_all_recipes()

        return render_template('dashboard.html', newUser=newUser, all_recipes=all_recipes)


################################################################################################################ <<GET/POST>> Route to log out
@app.route('/logout')
def logout():
    session.clear()
    # may require session.pop('first_name / or other key:id') #
    return redirect('/')


################################################################################################################

################################################################################################################ 


################################################################################################################ 


################################################################################################################ 


################################################################################################################ 



