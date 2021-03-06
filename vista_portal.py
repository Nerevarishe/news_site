from app import create_app, db, cli  # Do NOT remove cli import!!!
from app.models import User

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


# # PyCharm runner:
# if __name__ == '__main__':
#     app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
