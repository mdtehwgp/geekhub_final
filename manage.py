import os
from random import randrange
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Role, Post

if os.path.exists('.venv'):
    print('Importing environment from .venv...')
    for line in open('.venv'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db, render_as_batch=True)
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post)


@manager.command
def seed(Role=Role):
    """- insert roles"""
    Role.insert_roles()


@manager.command
def generate_fake():
    """- insert fake users"""
    from random import seed, randint
    import forgery_py
    from sqlalchemy.exc import IntegrityError
    COUNT = 5

    seed()
    for i in range(COUNT):
        u = User(email=forgery_py.internet.email_address(),
                 username=forgery_py.internet.user_name(True),
                 password="password",
                 confirmed=True,
                 name=forgery_py.name.full_name(),
                 location=forgery_py.address.city(),
                 performance_story_points=randrange(500, 1000, 10),
                 about_me=forgery_py.lorem_ipsum.sentence(),
                 member_since=forgery_py.date.date(True))
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    seed()
    user_count = User.query.count()
    for i in range(COUNT):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                 task_name='task #{}'.format(randint(1, 20)),
                 task_story_points=randrange(10, 1000, 10),
                 timestamp=forgery_py.date.date(True),
                 author=u)
        db.session.add(p)
        db.session.commit()


manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
