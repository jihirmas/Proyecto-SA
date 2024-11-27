# run both flask files

from model_submission import app as model_submission_app
from user_auth import app as user_auth_app

if __name__ == '__main__':
    model_submission_app.run(debug=True)
    user_auth_app.run(debug=True)