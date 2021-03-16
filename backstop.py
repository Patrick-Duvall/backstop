from app.__init__ import create_app, db
from app.models import User


application = create_app()

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
