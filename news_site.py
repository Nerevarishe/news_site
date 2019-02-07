from app import app, db, cli  # Do NOT remove cli import!!!
from app.models import User, News


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'News': News}


# PyCharm runner:
if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
