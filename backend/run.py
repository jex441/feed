import sys
import os
from flask_apscheduler import APScheduler

# This tells Python: treat /backend as the root.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from app import app
from app import get_data  # This is importing a module, not a function

# Initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)

# Add job to run every 3 seconds
@scheduler.task('interval', id='get_data_job', minutes=10, misfire_grace_time=900)
def scheduled_task():
    with app.app_context():
        get_data.get_data()

if __name__ == "__main__":
    scheduler.start()
    app.run(host='127.0.0.1', port=5000, debug=True)