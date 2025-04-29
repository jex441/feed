import sys
import os

# This tells Python: treat /backend as the root.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app
from app import routes  # Import routes after creating app

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
