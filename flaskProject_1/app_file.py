from app.models import User, Role
from app import create_app, db
from flask_migrate import Migrate
import unittest

flask_app = create_app('default')
migrate = Migrate(flask_app, db)

"""
@flask_app.shell_context_processors
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
"""

@flask_app.cli.command('test')
def test():
    """What we run"""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)





