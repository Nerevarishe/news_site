from app import app, db, cli
from app.models import User, News
import os


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'News': News}


# PyCharm runner:

#if __name__ == '__main__':
#    app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)

# c9.io runner

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), 
            debug=True, use_debugger=False, use_reloader=False, 
            passthrough_errors=True)
