#!/usr/bin/env python3

import os
import glob

import dotenv
dotenv.load_dotenv()

from agenda import init_app

APP_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_FILES = [f for f in glob.glob(f"{APP_DIR}/agenda/templates/*.ezt")]

app = init_app(APP_DIR)

if __name__ == "__main__":
    app.run(port=app.config['SERVER_PORT'], extra_files=TEMPLATE_FILES)
