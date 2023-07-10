"""run.py"""
import os
from api import app

# app = create_app(os.environ.get('environment_variable')or 'testing')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
