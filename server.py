from flask_app import app


# adjust names of controllers
from flask_app.controllers import user_controller
from flask_app.controllers import recipe_controller


# make sure port on Mac is set to number other than 5000
if __name__ == "__main__":
    app.run(debug=True, port=5001)




    
# =========================================================
# REMEMBER TO IMPORT CONTROLLERS INTO YOUR SERVER FILE!
# =========================================================

# from flask_app.controllers import

# RUN pipenv install PyMySQL flask flask-bcrypt

# REMEMBER TO SAVE YOUR .mwb FILE TO THE FOLDER! (erd diagram)
# REMEMBER TO SAVE YOUR .sql FILE TO THE FOLDER! (sql code)

