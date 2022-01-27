import os
import agenda

app = agenda.create_app(os.getenv('FLASK_CONFIG') or 'default')
