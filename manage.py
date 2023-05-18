import os
from flask_script import Manager
import unittest
from app import blueprint
from app.main import create_app
from flask_migrate import Migrate, MigrateCommand
from app.main import db
from app.main.model import student
from flask import Flask
from flask.cli import FlaskGroup


app = Flask(__name__)

app = create_app()
app.register_blueprint(blueprint)

app.app_context().push()
manager = Manager(app)

cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()


@manager.command
def run():
    app.run()

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()

