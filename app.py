from MyApp import create_app
from MyApp.BackEnd.Database.ProjectDatabase import db

app = create_app()

if __name__ == '__main__':

    # create table if not exist
    with app.app_context():
        db.create_all()


    app.run(debug=True, port=5000, host='0.0.0.0')